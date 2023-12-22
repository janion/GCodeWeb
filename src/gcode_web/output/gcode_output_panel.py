import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, render


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
                    ui.download_button(id=f'download_{file.title}', label="Download"),
                    [[ui.br(), line] for line in file.lines]
                ) for file in files]
            )
