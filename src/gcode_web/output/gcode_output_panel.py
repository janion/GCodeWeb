import io
import zipfile

from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_file_output_panel import gcode_file_output_panel_ui, gcode_file_output_panel_server


@module.ui
def gcode_output_panel_ui():
    return ui.output_ui(id='panel')


@module.server
def gcode_output_panel_server(input: Inputs, output: Outputs, session: Session, generated_files):
    @render.ui
    def panel():
        files = generated_files.get()

        if len(files) == 0:
            return ui.div(
                ui.p('No files generated'),
                style='text-align: center'
            )
        else:
            return ui.div(
                ui.download_button(id='download_all_btn', label="Download All"),
                ui.navset_tab(
                    *[ui.nav_panel(
                        file.name,
                        gcode_file_output_panel_ui(id=f'output_{file.title}')
                    ) for file in files]
                )
            )

    @reactive.Effect
    @reactive.event(generated_files)
    def _install_servers():
        for file in generated_files.get():
            gcode_file_output_panel_server(id=f'output_{file.title}', generated_file=file)

        if len(generated_files.get()) > 0:
            @session.download(filename="all_jobs.zip")
            async def download_all_btn():
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for file in generated_files.get():
                        zip_file.writestr(file.name, '\n'.join(file.lines))

                yield zip_buffer.getvalue()
