from shiny import Inputs, Outputs, Session, ui, reactive, module, render

from gcode_web.output.gcode_config import GCodeConfig


@module.ui
def job_name_ui(job: GCodeConfig):
    return ui.div(
        ui.input_text(id='job_name', label='Name', value=job.name),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def job_name_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names: reactive.Value[list[str]]):

    job_name = reactive.Value(job.name)
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    @reactive.event(input.job_name, ignore_init=True)
    def _set_name():
        job.name = input.job_name()
        job_name.set(input.job_name())

    @reactive.Effect
    @reactive.event(input.job_name, job_names)
    def _validate_job_name():
        if input.job_name() == '':
            error_msg.set('Job must have name')
        elif job_names.get().count(input.job_name()) > 1:
            error_msg.set('Job must have unique name')
        else:
            error_msg.set('')

    @render.text
    def error():
        return error_msg.get()

    return job_name
