from dataclasses import dataclass

from shiny import Inputs, Outputs, Session, ui, reactive, module

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server
from gcode_web.operation.display_names import get_display_name
from gcode_web.operation.remove_operation_link import remove_operation_ui, remove_operation_server
from gcode_web.job_name_panel import job_name_ui, job_name_server

from gcode_web.operation.circular_pocket import circular_pocket_ui, circular_pocket_server
from gcode_web.operation.rectangular_pocket import rectangular_pocket_ui, rectangular_pocket_server
from gcode_web.operation.circular_profile import circular_profile_ui, circular_profile_server
from gcode_web.operation.rectangular_profile import rectangular_profile_ui, rectangular_profile_server
from gcode_web.operation.drill import drill_ui, drill_server

from conversational_gcode.operations.pocket.CircularPocket import CircularPocket
from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket
from conversational_gcode.operations.profile.CircularProfile import CircularProfile
from conversational_gcode.operations.profile.RectangularProfile import RectangularProfile
from conversational_gcode.operations.Drill import Drill


_job_options_display_name = 'Job Options'
_tool_options_display_name = 'Tool Options'


def _create_operation_ui(id, operation):
    if isinstance(operation, CircularPocket):
        return circular_pocket_ui(id=id, config=operation)
    elif isinstance(operation, RectangularPocket):
        return rectangular_pocket_ui(id=id, config=operation)
    elif isinstance(operation, CircularProfile):
        return circular_profile_ui(id=id, config=operation)
    elif isinstance(operation, RectangularProfile):
        return rectangular_profile_ui(id=id, config=operation)
    elif isinstance(operation, Drill):
        return drill_ui(id=id, config=operation)
    return None


def _create_operation_server(op_id, del_id, job, operation):
    if isinstance(operation.operation, CircularPocket):
        circular_pocket_server(id=op_id, config=operation.operation)
    elif isinstance(operation.operation, RectangularPocket):
        rectangular_pocket_server(id=op_id, config=operation.operation)
    elif isinstance(operation.operation, CircularProfile):
        circular_profile_server(id=op_id, config=operation.operation)
    elif isinstance(operation.operation, RectangularProfile):
        rectangular_profile_server(id=op_id, config=operation.operation)
    elif isinstance(operation.operation, Drill):
        drill_server(id=op_id, config=operation.operation)

    delete = remove_operation_server(id=del_id)

    @reactive.Effect
    @reactive.event(delete)
    def _remove():
        if operation in job.operations:
            print(f'Removing Operation #{operation.id} from Job #{job.id}')
            job.operations.remove(operation)
            ui.remove_accordion_panel(id='accordion', target=op_id)
        _remove.destroy()


@module.ui
def job_ui(job: GCodeConfig):

    @dataclass
    class Item:
        name: str
        id: str
        ui: ui.Tag
        close_link: ui.Tag

    names_ids_and_uis = []

    id = 'job'
    names_ids_and_uis.append(Item(_job_options_display_name, id, job_options_ui(id=id, job=job), None))
    # Open job options if no operations added
    last_id = id
    ui.update_accordion(id='accordion', show=last_id)

    id = 'tool'
    names_ids_and_uis.append(Item(_tool_options_display_name, id, tool_options_ui(id=id, config=job.tool_config), None))

    for config in job.operations:
        id = f'op_{config.id}'
        last_id = config.id
        names_ids_and_uis.append(
            Item(
                get_display_name(type(config.operation)),
                id,
                _create_operation_ui(id, config.operation),
                remove_operation_ui(id=f'del_{config.id}')
            )
        )

    return ui.div(
        job_name_ui(id='name', job=job),
        ui.accordion(
            id='accordion',
            open=last_id,
            *[ui.accordion_panel(
                item.name,
                item.ui,
                value=item.id,
                icon=item.close_link
            ) for item in names_ids_and_uis]
        )
    )

@module.server
def job_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names: reactive.Value[list[str]], added_operation: reactive.Value[tuple[GCodeConfig, object]]):

    job_name = job_name_server(id='name', job=job, job_names=job_names)
    job_options_server(id='job', job=job)
    tool_options_server(id='tool', config=job.tool_config)

    for config in job.operations:
        _create_operation_server(f'op_{config.id}', f'del_{config.id}', job, config)

    @reactive.Effect
    @reactive.event(added_operation, ignore_none=True)
    def _add_operation():
        updated_job, operation = added_operation()
        if updated_job is job:
            print(f'Adding Operation #{operation.id} to Job #{job.id}')
            op_id = f'op_{operation.id}'
            del_id = f'del_{operation.id}'
            panel = ui.accordion_panel(
                get_display_name(type(operation.operation)),
                _create_operation_ui(op_id, operation.operation),
                value=op_id,
                icon=remove_operation_ui(id=del_id)
            )
            ui.insert_accordion_panel(id='accordion', panel=panel)

            _create_operation_server(op_id, del_id, job, operation)
            # TODO: This shouldn't be needed if ignore_init=True, but for some reason, it still is
            added_operation.set(None)

    return job_name
