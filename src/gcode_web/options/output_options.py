from shiny import Inputs, Outputs, Session, ui, module, reactive, render_text, render

from conversational_gcode.options.OutputOptions import OutputOptions


class OutputOptionsConfig:

    def __init__(self):
        self._position_precision = 3
        self._feed_precision = 2
        self._speed_precision = 1

    def _set_position_precision(self, value):
        self._position_precision = value

    def _set_feed_precision(self, value):
        self._feed_precision = value

    def _set_speed_precision(self, value):
        self._speed_precision = value

    position_precision = property(
        fget=lambda self: self._position_precision,
        fset=_set_position_precision
    )

    feed_precision = property(
        fget=lambda self: self._feed_precision,
        fset=_set_feed_precision
    )

    speed_precision = property(
        fget=lambda self: self._speed_precision,
        fset=_set_speed_precision
    )


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
def output_options_server(input: Inputs, output: Outputs, session: Session, config: OutputOptionsConfig):
    operation = reactive.Value()
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
        try:
            error_msg.set('')
            operation.set(OutputOptions(config.position_precision, config.feed_precision, config.speed_precision))
        except ValueError as exptn:
            error_msg.set(str(exptn))
            operation.set(None)

    @output
    @render.text
    def error():
        return error_msg.get()

    return operation
