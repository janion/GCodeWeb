from shiny import Inputs, Outputs, Session, ui, module, render


@module.ui
def gcode_file_output_panel_ui():
    return ui.div(
        ui.download_button(id=f'download_btn', label="Download"),
        ui.output_ui(id="file_contents")
    )


@module.server
def gcode_file_output_panel_server(input: Inputs, output: Outputs, session: Session, generated_file):
    @render.ui
    def file_contents():
        content = []
        for line in generated_file.lines:
            content.append(ui.br())

            # Display comment after first ';' in green
            split = line.split(';')
            content.append(split[0])
            content.append(';')
            comment = ';'.join(split[1:])
            content.append(ui.div(comment, {'style': 'color: #447744; display: inline-block'}))
        return content

    @session.download(filename=generated_file.name)
    async def download_btn():
        yield '\n'.join(generated_file.lines)
