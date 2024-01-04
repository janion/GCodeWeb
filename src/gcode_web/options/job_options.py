from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from gcode_web.output.gcode_config import GCodeConfig


@module.ui
def job_options_ui(job: GCodeConfig):
    config = job.job_config
    return ui.div(
        ui.input_numeric(id='clearance_height', label='Clearance Height', value=config.clearance_height),
        ui.input_numeric(id='lead_in', label='Lead-in', value=config.lead_in),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def job_options_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig):
    config = job.job_config

    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def set_clearance_height():
        config.clearance_height = input.clearance_height()

    @reactive.Effect(priority=1)
    def set_lead_in():
        config.lead_in = input.lead_in()

    @reactive.Effect
    @reactive.event(input.clearance_height, input.lead_in)
    def _validate_options():
        results = list(filter(lambda result: not result.success, config.validate()))

        if len(results) == 0:
            error_msg.set('')
        else:
            error_msg.set(results[0].message)

    @output
    @render.text
    def error():
        return error_msg.get()
