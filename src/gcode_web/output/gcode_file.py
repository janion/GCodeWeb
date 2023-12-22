class GcodeFile:
    def __init__(self, title, lines):
        self._title = title
        self._lines = lines

    title = property(fget=lambda self: self._title)
    name = property(fget=lambda self: f'{self._title}.nc')
    lines = property(fget=lambda self: self._lines)
