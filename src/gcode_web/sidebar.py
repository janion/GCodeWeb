import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.output_options import OutputOptionsConfig, output_options_ui, output_options_server


def _create_new_job():
    return GCodeConfig()


@module.ui
def sidebar_ui():
    return x.ui.sidebar(
        ui.input_action_button(id='clear_btn', label='Clear'),
        ui.input_action_button(id='load_jobs_btn', label='Load Jobs'),
        ui.input_action_button(id='new_job_btn', label='New Job'),
        ui.hr(),
        ui.input_select(
            id='operation_type',
            label='Operation',
            choices=[
                'Rectangular Pocket',
                'Circular Pocket',
                'Rectangular Profile',
                'Circular Profile'
            ]
        ),
        ui.input_action_button(id='new_operation', label='Add Operation'),
        ui.hr(),
        x.ui.accordion_panel(
            'Output Options',
            output_options_ui(id='output_options')
        ),
        ui.input_action_button(id='save_jobs', label='Save Jobs')
    )


@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session, job_configurations):
    output_options = OutputOptionsConfig()

    output_options_server(id='output_options', config=output_options)

    @reactive.Effect
    @reactive.event(input.new_job_btn)
    def _add_job():
        job_configurations.set(job_configurations.get() + [_create_new_job()])
