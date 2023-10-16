import shiny.experimental as x
from shiny import App, Inputs, Outputs, Session, ui, reactive

from gcode_web.sidebar import sidebar_ui, sidebar_server
from gcode_web.config_panel import config_panel_ui, config_panel_server
from gcode_web.output.gcode_output_panel import gcode_output_panel_ui, gcode_output_panel_server
from gcode_web.output.gcode_file import GcodeFile

app_ui = x.ui.page_sidebar(
    sidebar_ui(id='sidebar'),
    ui.page_fluid(
        ui.row(
            ui.column(
                6,
                config_panel_ui('config_panel')
            ),
            ui.column(
                6,
                gcode_output_panel_ui(id='gcode_panel')
            )
        )
    ),
    title='Conversational GCode'
)


def app_server(input: Inputs, output: Outputs, session: Session):
    job_configurations = reactive.Value([])

    config_tabs = config_panel_server(id='config_panel', job_configurations=job_configurations)
    generated_files = sidebar_server(id='sidebar', config_tabs=config_tabs, job_configurations=job_configurations)
    gcode_output_panel_server(id='gcode_panel', generated_files=generated_files)


def launch_app():
    return App(app_ui, app_server)
