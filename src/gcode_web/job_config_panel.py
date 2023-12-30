from shiny import App, Inputs, Outputs, Session, ui, reactive, render, module

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server
from gcode_web.operation.circular_pocket import circular_pocket_ui, circular_pocket_server
from gcode_web.operation.display_names import get_display_name

from conversational_gcode.operations.CircularPocket import CircularPocket


_job_options_display_name = 'Job Options'
_tool_options_display_name = 'Tool Options'


@module.ui
def job_ui(job: GCodeConfig):
    names_ids_and_uis = []
    config_index = 0

    id = f'job_{config_index}'
    names_ids_and_uis.append((_job_options_display_name, id, job_options_ui(id=id, job=job)))
    # Open job options if no operations added
    last_id = id
    ui.update_accordion(id='accordion', show=last_id)
    config_index += 1

    id = f'tool_{config_index}'
    names_ids_and_uis.append((_tool_options_display_name, id, tool_options_ui(id=id, config=job.tool_config)))
    config_index += 1

    for config in job.operations:
        id = f'op_{config_index}'
        last_id = id
        if isinstance(config, CircularPocket):
            names_ids_and_uis.append((get_display_name(type(config)), id, circular_pocket_ui(id=id, config=config)))
        config_index += 1

    return ui.accordion(
        id='accordion',
        open=last_id,
        *[ui.accordion_panel(name, each_ui, value=id) for name, id, each_ui in names_ids_and_uis]
    )

@module.server
def job_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names: reactive.Value[list[str]]):

    config_index = 0
    job_name = job_options_server(
        id=f'job_{config_index}',
        job=job,
        job_names=job_names
    )
    config_index += 1

    tool_options_server(id=f'tool_{config_index}', config=job.tool_config)
    config_index += 1

    for config in job.operations:
        if isinstance(config, CircularPocket):
            circular_pocket_server(id=f'op_{config_index}', config=config)
        config_index += 1

    return job_name
