from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from gcode_web.output.gcode_config import GCodeConfig


@module.ui
def job_options_ui(job: GCodeConfig):
    print(f'UI #{job.id} {job.job_config.name}')
    config = job.job_config
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
def job_options_server(input: Inputs, output: Outputs, session: Session, job: GCodeConfig, job_names):
    print(f'Server #{job.id} - {job.job_config.name}')
    config = job.job_config

    error_msg = reactive.Value('')
    job_name = reactive.Value(config.name)

    @reactive.Effect(priority=1)
    @reactive.event(input.job_name, ignore_init=True)
    def set_name():
        old_name = config.name

        config.name = input.job_name()
        job_name.set(input.job_name())

        if old_name == config.name:
            return

        print(f'Setting job name #{job.id}: {old_name} -> {config.name}')

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

    return job_name
