class GcodeFile:
    def __init__(self, name, lines):
        self._name = name
        self._lines = lines

    name = property(fget=lambda self: self._name)
    lines = property(fget=lambda self: self._lines)
