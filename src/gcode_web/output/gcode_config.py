from conversational_gcode.options.JobOptions import JobOptions
from conversational_gcode.options.ToolOptions import ToolOptions


class GCodeConfig:

    _ID = 0

    def __init__(self):
        self._id = GCodeConfig._ID
        GCodeConfig._ID += 1
        self._name = f'Job_{self._id}'
        self._job_config = JobOptions()
        self._tool_config = ToolOptions()
        self._operations = []

    def _set_name(self, value):
        self._name = value

    def _set_tool_config(self, tool_config):
        self._tool_config = tool_config

    name = property(
        fget=lambda self: self._name,
        fset=_set_name
    )
    id = property(
        fget=lambda self: self._id
    )
    job_config = property(
        fget=lambda self: self._job_config
    )
    tool_config = property(
        fget=lambda self: self._tool_config,
        fset=_set_tool_config
    )
    operations = property(
        fget=lambda self: self._operations
    )
