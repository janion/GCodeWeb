from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.options.ToolOptions import ToolOptions


_CONVENTIONAL = 'Conventional'
_CLIMB = 'Climb'


@module.ui
def tool_options_ui(config: ToolOptions):
    finishing_pass_type = _CLIMB if config.finishing_climb else _CONVENTIONAL
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

        ui.input_numeric(id='finishing_pass', label='Finishing Pass Stepover', value=config.finishing_pass),
        ui.input_numeric(id='finishing_feed_rate', label='Finishing Feed Rate', value=config.finishing_feed_rate),
        ui.input_select(
            id='finishing_climb',
            label='Finishing Pass Direction',
            choices=[_CONVENTIONAL, _CLIMB],
            selected=finishing_pass_type
        ),

        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def tool_options_server(input: Inputs, output: Outputs, session: Session, config: ToolOptions):
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
        config.finishing_climb = input.finishing_climb() == _CLIMB

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
        results = list(filter(lambda result: not result.success, config.validate()))

        if len(results) == 0:
            error_msg.set('')
        else:
            error_msg.set(results[0].message)

    @output
    @render.text
    def error():
        return error_msg.get()
