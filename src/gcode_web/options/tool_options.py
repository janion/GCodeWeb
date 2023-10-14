from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.options.ToolOptions import ToolOptions
class ToolOptionsConfig:

    display_name = 'Tool Options'

    def __init__(self):
        self._tool_flutes = 4
        self._tool_diameter = 6

        self._spindle_speed = 1000
        self._feed_rate = 100

        self._max_stepover = 3
        self._max_stepdown = 3

        self._max_helix_stepover = 2
        self._helix_feed_rate = 100
        self._max_helix_angle = 3

        self._finishing_pass = False
        self._finishing_feed_rate = 75
        self._finishing_climb = False

    def _set_tool_flutes(self, value):
        self._tool_flutes = value

    def _set_tool_diameter(self, value):
        self._tool_diameter = value

    def _set_spindle_speed(self, value):
        self._spindle_speed = value

    def _set_feed_rate(self, value):
        self._feed_rate = value

    def _set_max_stepover(self, value):
        self._max_stepover = value

    def _set_max_stepdown(self, value):
        self._max_stepdown = value

    def _set_max_helix_stepover(self, value):
        self._max_helix_stepover = value

    def _set_helix_feed_rate(self, value):
        self._helix_feed_rate = value

    def _set_max_helix_angle(self, value):
        self._max_helix_angle = value

    def _set_finishing_pass(self, value):
        self._finishing_pass = value

    def _set_finishing_feed_rate(self, value):
        self._finishing_feed_rate = value

    def _set_finishing_climb(self, value):
        self._finishing_climb = value

    tool_flutes = property(
        fget=lambda self: self._tool_flutes,
        fset=_set_tool_flutes
    )
    tool_diameter = property(
        fget=lambda self: self._tool_diameter,
        fset=_set_tool_diameter
    )

    spindle_speed = property(
        fget=lambda self: self._spindle_speed,
        fset=_set_spindle_speed
    )
    feed_rate = property(
        fget=lambda self: self._feed_rate,
        fset=_set_feed_rate
    )

    max_stepover = property(
        fget=lambda self: self._max_stepover,
        fset=_set_max_stepover
    )
    max_stepdown = property(
        fget=lambda self: self._max_stepdown,
        fset=_set_max_stepdown
    )

    max_helix_stepover = property(
        fget=lambda self: self._max_helix_stepover,
        fset=_set_max_helix_stepover
    )
    helix_feed_rate = property(
        fget=lambda self: self._helix_feed_rate,
        fset=_set_helix_feed_rate
    )
    max_helix_angle = property(
        fget=lambda self: self._max_helix_angle,
        fset=_set_max_helix_angle
    )

    finishing_pass = property(
        fget=lambda self: self._finishing_pass,
        fset=_set_finishing_pass
    )
    finishing_feed_rate = property(
        fget=lambda self: self._finishing_feed_rate,
        fset=_set_finishing_feed_rate
    )
    finishing_climb = property(
        fget=lambda self: self._finishing_climb,
        fset=_set_finishing_climb
    )


@module.ui
def tool_options_ui(config: ToolOptionsConfig):
    return ui.div(
        ui.input_numeric(id='tool_flutes', label='Tool Flutes', value=config.tool_flutes),
        ui.input_numeric(id='tool_diameter', label='Tool Diameter', value=config.tool_diameter),

        ui.input_numeric(id='spindle_speed', label='Spindle Speed', value=config.spindle_speed),
        ui.input_numeric(id='feed_rate', label='Feed Rate', value=config.feed_rate),

        ui.input_numeric(id='max_stepover', label='Max Stepover', value=config.max_stepover),
        ui.input_numeric(id='max_stepdown', label='Max Stepdown', value=config.max_stepdown),

        ui.input_numeric(id='max_helix_stepover', label='Max Helical Stepover', value=config.max_helix_stepover),
        ui.input_numeric(id='helix_feed_rate', label='Helical Feed Rate', value=config.helix_feed_rate),
        ui.input_numeric(id='max_helix_angle', label='Max Helix Angle', value=config.max_helix_angle),

        ui.input_checkbox(id='finishing_pass', label='Has Finishing Pass', value=config.finishing_pass),
        ui.input_numeric(id='finishing_feed_rate', label='Finishing Feed Rate', value=config.finishing_feed_rate),
        ui.input_checkbox(id='finishing_climb', label='Finishing Pass is Climb', value=config.finishing_climb),

        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def tool_options_server(input: Inputs, output: Outputs, session: Session, config: ToolOptionsConfig):
    operation = reactive.Value()
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def set_clearance_height():
        config.clearance_height = input.clearance_height()

    @reactive.Effect(priority=1)
    def set_tool_flutes():
        config.tool_flutes = input.tool_flutes()

    @reactive.Effect(priority=1)
    def set_tool_diameter():
        config.tool_diameter = input.tool_diameter()

    @reactive.Effect(priority=1)
    def set_spindle_speed():
        config.spindle_speed = input.spindle_speed()

    @reactive.Effect(priority=1)
    def set_feed_rate():
        config.feed_rate = input.feed_rate()

    @reactive.Effect(priority=1)
    def set_max_stepover():
        config.max_stepover = input.max_stepover()

    @reactive.Effect(priority=1)
    def set_max_stepdown():
        config.max_stepdown = input.max_stepdown()

    @reactive.Effect(priority=1)
    def set_max_helix_stepover():
        config.max_helix_stepover = input.max_helix_stepover()

    @reactive.Effect(priority=1)
    def set_helix_feed_rate():
        config.helix_feed_rate = input.helix_feed_rate()

    @reactive.Effect(priority=1)
    def set_max_helix_angle():
        config.max_helix_angle = input.max_helix_angle()

    @reactive.Effect(priority=1)
    def set_finishing_pass():
        config.finishing_pass = input.finishing_pass()

    @reactive.Effect(priority=1)
    def set_finishing_feed_rate():
        config.finishing_feed_rate = input.finishing_feed_rate()

    @reactive.Effect(priority=1)
    def set_finishing_climb():
        config.finishing_climb = input.finishing_climb()

    @reactive.Effect
    @reactive.event(
        input.tool_flutes,
        input.tool_diameter,
        input.spindle_speed,
        input.feed_rate,
        input.max_stepover,
        input.max_stepdown,
        input.max_helix_stepover,
        input.helix_feed_rate,
        input.max_helix_angle,
        input.finishing_pass,
        input.finishing_feed_rate,
        input.finishing_climb
    )
    def calculate_operation():
        try:
            error_msg.set('')
            operation.set(
                ToolOptions(
                    input.tool_flutes(),
                    input.tool_diameter(),
                    input.spindle_speed(),
                    input.feed_rate(),
                    input.max_stepover(),
                    input.max_stepdown(),
                    input.max_helix_stepover(),
                    input.helix_feed_rate(),
                    input.max_helix_angle(),
                    input.finishing_pass(),
                    input.finishing_feed_rate(),
                    input.finishing_climb()
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
