from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.operations.CircularPocket import CircularPocket


@module.ui
def circular_pocket_ui(config: CircularPocket):
    return ui.div(
        ui.p('Centre'),
        ui.input_numeric(id='centre_x', label='X', value=config.centre[0]),
        ui.input_numeric(id='centre_y', label='Y', value=config.centre[1]),
        ui.input_numeric(id='start_depth', label='Start Depth', value=config.start_depth),
        ui.input_numeric(id='diameter', label='Diameter', value=config.diameter),
        ui.input_numeric(id='depth', label='Depth', value=config.depth),
        ui.input_checkbox(id='finishing_pass', label='Has Finishing Pass', value=config.finishing_pass),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def circular_pocket_server(input: Inputs, output: Outputs, session: Session, config: CircularPocket):
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def _set_centre():
        config.centre = [input.centre_x(), input.centre_y()]

    @reactive.Effect(priority=1)
    def _set_start_depth():
        config.start_depth = input.start_depth()

    @reactive.Effect(priority=1)
    def _set_diameter():
        config.diameter = input.diameter()

    @reactive.Effect(priority=1)
    def _set_finishing_pass():
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
    def _validate_operation():
        results = list(filter(lambda result: not result.success, config.validate()))

        if len(results) == 0:
            error_msg.set('')
        else:
            error_msg.set(results[0].message)

    @output
    @render.text
    def error():
        return error_msg.get()
