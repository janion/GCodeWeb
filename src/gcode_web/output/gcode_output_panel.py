from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_file_output_panel import gcode_file_output_panel_ui, gcode_file_output_panel_server


@module.ui
def gcode_output_panel_ui():
    return ui.output_ui(id='panel')


@module.server
def gcode_output_panel_server(input: Inputs, output: Outputs, session: Session, generated_files):
    @output
    @render.ui
    def panel():
        files = generated_files.get()

        if len(files) == 0:
            return ui.div(
                ui.p('No files generated'),
                style='text-align: center'
            )
        else:
            return ui.navset_tab(
                *[ui.nav(
                    file.name,
                    gcode_file_output_panel_ui(id=f'output_{file.title}')
                ) for file in files]
            )

    @reactive.Effect
    @reactive.event(generated_files)
    def _install_servers():
        for file in generated_files.get():
            gcode_file_output_panel_server(id=f'output_{file.title}', generated_file=file)
