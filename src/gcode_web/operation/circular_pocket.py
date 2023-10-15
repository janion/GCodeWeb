from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.operations.CircularPocket import CircularPocket


class CircularPocketConfig:

    display_name = 'Circular Pocket'

    def __init__(self):
        self._centre = [0, 0]
        self._start_depth = 0
        self._diameter = 10
        self._depth = 3
        self._finishing_pass = False

    def _set_centre(self, value):
        self._centre = value

    def _set_start_depth(self, value):
        self._start_depth = value

    def _set_diameter(self, value):
        self._diameter = value

    def _set_depth(self, value):
        self._depth = value

    def _set_finishing_pass(self, value):
        self._finishing_pass = value

    centre = property(
        fget=lambda self: self._centre,
        fset=_set_centre
    )
    start_depth = property(
        fget=lambda self: self._start_depth,
        fset=_set_start_depth
    )
    diameter = property(
        fget=lambda self: self._diameter,
        fset=_set_diameter
    )
    depth = property(
        fget=lambda self: self._depth,
        fset=_set_depth
    )
    finishing_pass = property(
        fget=lambda self: self._finishing_pass,
        fset=_set_finishing_pass
    )


@module.ui
def circular_pocket_ui(config: CircularPocketConfig):
    return ui.div(
        ui.p('Centre'),
        ui.input_numeric(id='centre_x', label='X', value=config.centre[0]),
        ui.input_numeric(id='centre_y', label='Y', value=config.centre[1]),
        ui.input_numeric(id='start_depth', label='Start Depth', value=config.start_depth),
        ui.input_numeric(id='diameter', label='Diameter', value=config.diameter),
        ui.input_numeric(id='depth', label='Depth', value=config.depth),
        ui.input_checkbox(id='finishing_pass', label='Finishing Pass', value=config.finishing_pass),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def circular_pocket_server(input: Inputs, output: Outputs, session: Session, config: CircularPocketConfig):
    operation = reactive.Value()
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def set_clearance_height():
        config.centre = [input.centre_x(), input.centre_y()]

    @reactive.Effect(priority=1)
    def set_start_depth():
        config.start_depth = input.start_depth()

    @reactive.Effect(priority=1)
    def set_diameter():
        config.diameter = input.diameter()

    @reactive.Effect(priority=1)
    def set_finishing_pass():
        config.finishing_pass = input.finishing_pass()

    @reactive.Effect
    @reactive.event(
        input.centre_x,
        input.centre_y,
        input.start_depth,
        input.diameter,
        input.depth,
        input.finishing_pass
    )
    def calculate_operation():
        try:
            error_msg.set('')
            operation.set(
                CircularPocket(
                    config.centre,
                    config.start_depth,
                    config.diameter,
                    config.depth,
                    config.finishing_pass
                )
            )
        except ValueError as exptn:
            error_msg.set(str(exptn))
            operation.set(None)

    @output
    @render.text
    def error():
        return error_msg.get()

    return operation
