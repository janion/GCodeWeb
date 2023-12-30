from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.job_config_panel import job_config_panel_ui, job_config_panel_server


@module.ui
def job_config_tab_ui(job: GCodeConfig):
    return ui.nav_panel(
        ui.output_text(id='title'),
        job_config_panel_ui(id='config_panel', job=job)
    )


@module.server
def job_config_tab_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names: list, recalculate_job_names: reactive.Value, invalidated_job: reactive.Value):
    job_name = job_config_panel_server(
        id='config_panel',
        job=job,
        job_names=job_names,
        recalculate_job_names=recalculate_job_names,
        invalidated_job=invalidated_job
    )

    @output
    @render.text
    def title():
        return job_name.get()

    return job_name
