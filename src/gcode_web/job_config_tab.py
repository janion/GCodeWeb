from shiny import Inputs, Outputs, Session, ui, render, module

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.job_config_panel import job_ui, job_server


@module.ui
def job_tab_ui(job: GCodeConfig):
    return ui.nav_panel(
        ui.output_text(id='title'),
        job_ui(id='job', job=job),
        value=f'tab_{job.id}'
    )


@module.server
def job_tab_server(input: Inputs, output: Outputs, session: Session, job:GCodeConfig, job_names: list[str]):
    job_name = job_server(id='job', job=job, job_names=job_names)

    @render.text
    def title():
        return job_name.get()

    return job_name
