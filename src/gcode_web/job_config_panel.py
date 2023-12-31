from shiny import App, Inputs, Outputs, Session, ui, reactive, render, module

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server
from gcode_web.operation.circular_pocket import circular_pocket_ui, circular_pocket_server
from gcode_web.operation.display_names import get_display_name

from conversational_gcode.operations.CircularPocket import CircularPocket


_job_options_display_name = 'Job Options'
_tool_options_display_name = 'Tool Options'


def _create_operation_ui(id, operation):
    if isinstance(operation, CircularPocket):
        return circular_pocket_ui(id=id, config=operation)
    return None


def _create_operation_server(id, operation):
    if isinstance(operation, CircularPocket):
        return circular_pocket_server(id=id, config=operation)
    return None


@module.ui
def job_ui(job: GCodeConfig):
    names_ids_and_uis = []

    id = 'job'
    names_ids_and_uis.append((_job_options_display_name, id, job_options_ui(id=id, job=job)))
    # Open job options if no operations added
    last_id = id
    ui.update_accordion(id='accordion', show=last_id)

    id = 'tool'
    names_ids_and_uis.append((_tool_options_display_name, id, tool_options_ui(id=id, config=job.tool_config)))

    op_index = 0
    for config in job.operations:
        id = f'op_{op_index}'
        last_id = id
        names_ids_and_uis.append((get_display_name(type(config)), id, _create_operation_ui(id, config)))
        op_index += 1

    return ui.accordion(
        id='accordion',
        open=last_id,
        *[ui.accordion_panel(name, each_ui, value=id) for name, id, each_ui in names_ids_and_uis]
    )

@module.server
def job_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names: reactive.Value[list[str]], added_operation: reactive.Value[tuple[GCodeConfig, object]]):

    job_name = job_options_server(id='job', job=job, job_names=job_names)
    tool_options_server(id='tool', config=job.tool_config)

    config_index = 0
    for config in job.operations:
        _create_operation_server(f'op_{config_index}', config)
        config_index += 1

    @reactive.Effect
    def _add_operation():
        updated_job, operation = added_operation()
        if updated_job is job:
            id = f'op_{len(job.operations)}'
            panel = ui.accordion_panel(
                get_display_name(type(operation)),
                _create_operation_ui(id, operation),
                value=id
            )
            ui.insert_accordion_panel(id='accordion', panel=panel)

            _create_operation_server(id, operation)

    return job_name
