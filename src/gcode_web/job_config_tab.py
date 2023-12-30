from shiny import Inputs, Outputs, Session, ui, render, module, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.job_config_panel import job_ui, job_server


@module.ui
def job_tab_ui(job: GCodeConfig):
    return ui.nav_panel(
        ui.div(ui.output_text(id='title'), style='display: inline-block;'),
        job_ui(id='job', job=job),
        value=f'tab_{job.id}',
        icon=ui.input_action_button(id='close', label='✖', style='border: none; padding: 0; margin: 0 5px 0 0;')
    )


@module.server
def job_tab_server(input: Inputs, output: Outputs, session: Session, job:GCodeConfig, job_names: list[str], removed_job: reactive.Value[GCodeConfig]):
    @reactive.Effect
    @reactive.event(input.close)
    def _remove_job():
        removed_job.set(job)
        _remove_job.destroy()

    job_name = job_server(id='job', job=job, job_names=job_names)

    @render.text
    def title():
        return job_name.get()

    return job_name
