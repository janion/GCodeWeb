from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.options.JobOptions import JobOptions


@module.ui
def job_options_ui(config: JobOptions):
    return ui.div(
        ui.input_text(id='job_name', label='Name', value=config.name),
        ui.input_numeric(id='clearance_height', label='Clearance Height', value=config.clearance_height),
        ui.input_numeric(id='lead_in', label='Lead-in', value=config.lead_in),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def job_options_server(input: Inputs, output: Outputs, session: Session, config: JobOptions, job_names, recalculate_job_names):
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def set_name():
        config.name = input.job_name()
        recalculate_job_names.set(True)

    @reactive.Effect(priority=1)
    def set_clearance_height():
        config.clearance_height = input.clearance_height()

    @reactive.Effect(priority=1)
    def set_lead_in():
        config.lead_in = input.lead_in()

    @reactive.Effect
    @reactive.event(input.clearance_height, input.lead_in, input.job_name, job_names)
    def calculate_operation():
        if input.job_name() == '':
            error_msg.set('Job must have name')
        elif job_names.get().count(input.job_name()) > 1:
            error_msg.set('Job must have unique name')
        else:
            results = list(filter(lambda result: not result.success, config.validate()))

            if len(results) == 0:
                error_msg.set('')
            else:
                error_msg.set(results[0].message)

    @output
    @render.text
    def error():
        return error_msg.get()
