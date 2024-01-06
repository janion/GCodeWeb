from shiny import Inputs, Outputs, Session, ui, module, reactive, render

from conversational_gcode.operations.profile.RectangularProfile import RectangularProfile


_CENTRE = 'Centre'
_CORNER = 'Corner'

_INSIDE = 'Inside'
_OUTSIDE = 'Outside'


@module.ui
def rectangular_profile_ui(config: RectangularProfile):
    if config.centre is not None and None not in config.centre:
        selected_ref_type = _CENTRE
        ref = config.centre
    elif config.corner is not None and None not in config.corner:
        selected_ref_type = _CORNER
        ref = config.corner
    else:
        selected_ref_type = None
        ref = [None, None]

    return ui.div(
        ui.input_select(id='ref_type', label='Reference Location', choices=[_CENTRE, _CORNER], selected=selected_ref_type),
        ui.input_numeric(id='ref_x', label='X', value=ref[0]),
        ui.input_numeric(id='ref_y', label='Y', value=ref[1]),
        ui.input_numeric(id='width', label='Width', value=config.width),
        ui.input_numeric(id='length', label='Length', value=config.length),
        ui.input_numeric(id='depth', label='Depth', value=config.depth),
        ui.input_numeric(id='start_depth', label='Start Depth', value=config.start_depth),
        ui.input_select(
            id='in_out',
            label='Side',
            choices=[_INSIDE, _OUTSIDE],
            selected=_INSIDE if config.is_inner else _OUTSIDE
        ),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def rectangular_profile_server(input: Inputs, output: Outputs, session: Session, config: RectangularProfile):
    error_msg = reactive.Value('')

    @reactive.Effect(priority=1)
    def _set_reference():
        if input.ref_type() == _CENTRE:
            config.corner = None
            config.centre = [input.ref_x(), input.ref_y()]
        elif input.ref_type() == _CORNER:
            config.centre = None
            config.corner = [input.ref_x(), input.ref_y()]
        else:
            config.centre = None
            config.corner = None

    @reactive.Effect(priority=1)
    def _set_width():
        config.width = input.width()

    @reactive.Effect(priority=1)
    def _set_length():
        config.length = input.length()

    @reactive.Effect(priority=1)
    def _set_depth():
        config.depth = input.depth()

    @reactive.Effect(priority=1)
    def _set_start_depth():
        config.start_depth = input.start_depth()

    @reactive.Effect(priority=1)
    def _set_is_inner():
        config.is_inner = input.in_out() == _INSIDE

    @reactive.Effect
    @reactive.event(
        input.ref_type,
        input.ref_x,
        input.ref_y,
        input.width,
        input.length,
        input.depth,
        input.start_depth,
        input.in_out
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
