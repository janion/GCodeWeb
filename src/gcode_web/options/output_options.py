from shiny import Inputs, Outputs, Session, ui, module, reactive, render_text, render

from conversational_gcode.options.OutputOptions import OutputOptions


@module.ui
def output_options_ui():
    return ui.div(
        ui.input_numeric(id='position_precision', label='Position Decimal Places', value=1),
        ui.input_numeric(id='feed_precision', label='Feed Decimal Places', value=1),
        ui.input_numeric(id='speed_precision', label='Speed Decimal Places', value=1),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def output_options_server(input: Inputs, output: Outputs, session: Session, config: OutputOptions):
    error_msg = reactive.Value('')

    ui.update_numeric(id='position_precision', value=config.position_precision)
    ui.update_numeric(id='feed_precision', value=config.feed_precision)
    ui.update_numeric(id='speed_precision', value=config.speed_precision)

    @reactive.Effect(priority=1)
    def set_position_precision():
        config.position_precision = input.position_precision()

    @reactive.Effect(priority=1)
    def set_feed_precision():
        config.feed_precision = input.feed_precision()

    @reactive.Effect(priority=1)
    def set_speed_precision():
        config.speed_precision = input.speed_precision()

    @reactive.Effect
    @reactive.event(input.position_precision, input.feed_precision, input.speed_precision)
    def calculate_operation():
        results = list(filter(lambda result: not result.success, config.validate()))

        if len(results) == 0:
            error_msg.set('')
        else:
            error_msg.set(results[0].message)

    @output
    @render.text
    def error():
        return error_msg.get()
