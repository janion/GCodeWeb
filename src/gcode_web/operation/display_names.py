from conversational_gcode.operations.CircularPocket import CircularPocket
from conversational_gcode.operations.RectangularPocket import RectangularPocket
from conversational_gcode.operations.CircularProfile import CircularProfile


_display_names = {
    CircularPocket: 'Circular Pocket',
    RectangularPocket: 'Rectangular Pocket',
    CircularProfile: 'Circular Profile'
}

_types = {
    name: typee for typee, name in _display_names.items()
}


def get_display_name(operation_type):
    return _display_names[operation_type]


def get_type(operation_display_name):
    return _types[operation_display_name]
