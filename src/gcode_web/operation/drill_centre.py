from shiny import Inputs, Outputs, Session, ui, module, reactive


class DrillCentre:

    _ID = 0

    def __init__(self, coordinates: list[float] = None):
        self._id = DrillCentre._ID
        DrillCentre._ID += 1
        if coordinates is None:
            self.coordinates = [0, 0]
        else:
            self.coordinates = coordinates[:2]

    id = property(fget=lambda self: self._id)


@module.ui
def drill_centre_ui(centre: DrillCentre):
    return ui.div(
        ui.input_numeric(id='x', label='X', value=centre.coordinates[0]),
        ui.input_numeric(id='y', label='Y', value=centre.coordinates[1]),
        ui.input_action_button(id='delete', label='✖', style='border: none; padding: 0; margin: 0 5px 0 0;')
    )


@module.server
def drill_centre_server(input: Inputs, output: Outputs, session: Session, centre: DrillCentre):
    @reactive.Effect
    def _set_centre():
        centre.coordinates[0] = input.x()
        centre.coordinates[1] = input.y()

    return input.delete
