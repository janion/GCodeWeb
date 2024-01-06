from shiny import App, Inputs, Outputs, Session, ui, reactive

from gcode_web.sidebar import sidebar_ui, sidebar_server
from gcode_web.output.gcode_output_panel import gcode_output_panel_ui, gcode_output_panel_server

from gcode_web.config_panel import jobs_panel_ui, jobs_panel_server

app_ui = ui.page_sidebar(
    sidebar_ui(id='sidebar'),
    ui.page_fluid(
        ui.row(
            ui.column(
                6,
                jobs_panel_ui(id='config_panel')
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
    added_operation = reactive.Value()

    selected_job_id = jobs_panel_server(id='config_panel', jobs=job_configurations, added_operation=added_operation)
    generated_files = sidebar_server(id='sidebar', selected_job_id=selected_job_id, job_configurations=job_configurations, added_operation=added_operation)
    gcode_output_panel_server(id='gcode_panel', generated_files=generated_files)


def launch_app():
    return App(app_ui, app_server)
