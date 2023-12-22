import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server
from gcode_web.operation.circular_pocket import circular_pocket_ui, circular_pocket_server
from gcode_web.operation.display_names import get_display_name

from conversational_gcode.operations.CircularPocket import CircularPocket


_job_options_display_name = 'Job Options'
_tool_options_display_name = 'Tool Options'


@module.ui
def job_config_panel_ui(job: GCodeConfig):
    names_and_uis = []
    config_index = 0

    names_and_uis.append((_job_options_display_name, job_options_ui(id=f'job_{job.id}_{config_index}', config=job.job_config)))
    config_index += 1

    names_and_uis.append((_tool_options_display_name, tool_options_ui(id=f'job_{job.id}_{config_index}', config=job.tool_config)))
    config_index += 1

    for config in job.operations:
        if isinstance(config, CircularPocket):
            names_and_uis.append((get_display_name(type(config)), circular_pocket_ui(id=f'job_{job.id}_{config_index}', config=config)))
        config_index += 1

    return x.ui.accordion(
        *[x.ui.accordion_panel(name, each_ui) for name, each_ui in names_and_uis]
    )


@module.server
def job_config_panel_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names, recalculate_job_names):
    config_index = 0
    job_name = job_options_server(
        id=f'job_{job.id}_{config_index}',
        config=job.job_config,
        job_names=job_names
    )
    config_index += 1

    tool_options_server(id=f'job_{job.id}_{config_index}', config=job.tool_config)
    config_index += 1

    for config in job.operations:
        if isinstance(config, CircularPocket):
            circular_pocket_server(id=f'job_{job.id}_{config_index}', config=config)
        config_index += 1

    @reactive.Effect
    @reactive.event(job_name)
    def _force_job_names_recalculation():
        recalculate_job_names.set(True)

    @output
    @render.text
    def title():
        return job_name.get()

    return job_name
