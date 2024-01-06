from conversational_gcode.operations.pocket.CircularPocket import CircularPocket
from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket
from conversational_gcode.operations.profile.CircularProfile import CircularProfile
from conversational_gcode.operations.profile.RectangularProfile import RectangularProfile
from conversational_gcode.operations.Drill import Drill


_display_names = {
    CircularPocket: 'Circular Pocket',
    RectangularPocket: 'Rectangular Pocket',
    CircularProfile: 'Circular Profile',
    RectangularProfile: 'Rectangular Profile',
    Drill: 'Drill'
}

_types = {
    name: typee for typee, name in _display_names.items()
}


def get_display_name(operation_type):
    return _display_names[operation_type]


def get_type(operation_display_name):
    return _types[operation_display_name]
