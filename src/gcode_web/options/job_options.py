from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.options.JobOptions import JobOptions


class JobOptionsConfig:

    display_name = 'Job Options'

    def __init__(self):
        self._clearance_height = 10
        self._lead_in = 0.25

    def _set_clearance_height(self, value):
        self._clearance_height = value

    def _set_lead_in(self, value):
        self._lead_in = value

    clearance_height = property(
        fget=lambda self: self._clearance_height,
        fset=_set_clearance_height
    )

    lead_in = property(
        fget=lambda self: self._lead_in,
        fset=_set_lead_in
    )


@module.ui
def job_options_ui(config: JobOptionsConfig):
    return ui.div(
        ui.input_numeric(id='clearance_height', label='Clearance Height', value=config.clearance_height),
        ui.input_numeric(id='lead_in', label='Lead-in', value=config.lead_in),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def job_options_server(input: Inputs, output: Outputs, session: Session, config: JobOptionsConfig):
    operation = reactive.Value()
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def set_clearance_height():
        config.clearance_height = input.clearance_height()

    @reactive.Effect(priority=1)
    def set_lead_in():
        config.lead_in = input.lead_in()

    @reactive.Effect
    @reactive.event(input.clearance_height, input.lead_in)
    def calculate_operation():
        try:
            error_msg.set('')
            operation.set(JobOptions(config.clearance_height, config.lead_in))
        except ValueError as exptn:
            error_msg.set(str(exptn))
            operation.set(None)

    @output
    @render.text
    def error():
        return error_msg.get()

    return operation
