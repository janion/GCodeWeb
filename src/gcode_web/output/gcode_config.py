from gcode_web.options.job_options import JobOptionsConfig
from gcode_web.options.tool_options import ToolOptionsConfig


class GCodeConfig:

    def __init__(self):
        self._job_config = JobOptionsConfig()
        self._tool_config = ToolOptionsConfig()
        self._operations = []

    def _set_tool_config(self, tool_config):
        self._tool_config = tool_config

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
