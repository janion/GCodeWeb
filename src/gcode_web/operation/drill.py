from re import search, findall

from shiny import Inputs, Outputs, Session, ui, module, reactive, render

# from gcode_web.operation.drill_centre import drill_centre_ui, drill_centre_server, DrillCentre

from conversational_gcode.operations.Drill import Drill


# def _render_drill_centre_ui(centre: DrillCentre):
#     ui.insert_ui(
#         ui=ui.div(
#             drill_centre_ui(id=f'centre_{centre.id}', centre=centre),
#             id=f'centre_{centre.id}'
#         ),
#         selector='#centres_anchor',
#         where='beforeBegin'
#     )
#
#
# def _install_drill_centre_server(centre: DrillCentre, all_centres_reactive: reactive.Value[list[DrillCentre]]):
#     @reactive.Effect
#     def _install_server():
#         delete = drill_centre_server(id=f'centre_{centre.id}', centre=centre)
#
#         @reactive.Effect
#         @reactive.event(delete)
#         def _delete():
#             print(f'Removing Drill Centre #{centre.id}')
#             ui.remove_ui(selector=f'#centre_{centre.id}')
#             all_centres = all_centres_reactive()
#             all_centres.remove(centre)
#             all_centres_reactive.set([*all_centres])
#             _delete.destroy()


@module.ui
def drill_ui(config: Drill):
    return ui.div(
        ui.div(
            'Centres',
            # ui.div(
            #     ui.input_action_button(id='add_centre', label='+'),
            #     style='display: inline-block;'
            # ),
            # style='border-color: red; border-style: solid;'
        ),
        # *[_render_drill_centre_ui(centre) for centre in config.centres],
        # ui.div(id='centres_anchor'),
        ui.div(
            ui.input_text(
                id='text_centres',
                label='Centres',
                value=None if config.centres == [] else str(config.centres)[1:-1],
                placeholder='Eg. [20, 10], [110, -18]'),
            title='This is a temporary measure to work around limitations of the "Shiny" package'
        ),
        ui.input_numeric(id='start_depth', label='Start Depth', value=config.start_depth),
        ui.input_numeric(id='depth', label='Depth', value=config.depth),
        ui.input_numeric(id='peck_interval', label='Peck Interval', value=config.peck_interval),
        ui.input_numeric(id='dwell', label='Bottom Dwell', value=config.dwell),
        ui.div(
            ui.output_text(id='error'),
            style='color: red; font-style: italic;'
        )
    )


@module.server
def drill_server(input: Inputs, output: Outputs, session: Session, config: Drill):
    error_msg = reactive.Value('')

    # drill_centres = reactive.Value([DrillCentre(centre) for centre in config.centres])

    # No need to render centres when the UI is redrawn because they can only have been generated from here
    # TODO: This might need to be updated when save/load functionality is implemented
    # for centre in drill_centres():
    #     _render_drill_centre(centre, drill_centres)

    # @reactive.Effect
    # def _install_centre_servers():
    #     for centre in drill_centres():
    #         _render_drill_centre_ui(centre)
    #         _install_drill_centre_server(centre, drill_centres)
    #
    # @reactive.Effect
    # @reactive.event(input.add_centre)
    # def _add_centre():
    #     new_centre = DrillCentre()
    #     print(f'Adding Drill Centre #{new_centre.id}')
    #     drill_centres.set([*drill_centres(), new_centre])

    # @reactive.Effect()
    # def _set_centres():
    #     config.centres = [centre.coordinates for centre in drill_centres()]

    @reactive.Effect(priority=1)
    def _set_centres():
        text = input.text_centres().replace(' ', '')

        match = search('^(\\[-?[0-9]+,-?[0-9]+\\],?)+$', text)
        if match is None:
            config.centres = []
        else:
            config.centres = [eval(group) for group in findall('\\[-?[0-9]+,-?[0-9]+\\]', text)]

    @reactive.Effect(priority=1)
    def _set_start_depth():
        config.start_depth = input.start_depth()

    @reactive.Effect(priority=1)
    def _set_depth():
        config.depth = input.depth()

    @reactive.Effect(priority=1)
    def _set_peck_interval():
        config.peck_interval = input.peck_interval()

    @reactive.Effect(priority=1)
    def _set_dwell():
        config.dwell = 1000 * input.dwell() if input.dwell is not None else None

    @reactive.Effect
    @reactive.event(
        input.text_centres,
        input.start_depth,
        input.depth,
        input.peck_interval,
        input.dwell
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
