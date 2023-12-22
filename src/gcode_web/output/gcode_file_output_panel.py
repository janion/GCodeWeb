import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, render


@module.ui
def gcode_file_output_panel_ui():
    return ui.div(
        ui.download_button(id=f'download_btn', label="Download"),
        ui.output_ui(id="file_contents")
    )


@module.server
def gcode_file_output_panel_server(input: Inputs, output: Outputs, session: Session, generated_file):
    @output
    @render.ui
    def file_contents():
        return [[ui.br(), line] for line in generated_file.lines]

    @session.download(filename=generated_file.name)
    async def download_btn():
        yield '\n'.join(generated_file.lines)
