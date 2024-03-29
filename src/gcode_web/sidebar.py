import traceback
import sys

from shiny import Inputs, Outputs, Session, ui, module, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.output.gcode_file import GcodeFile
from gcode_web.options.output_options import output_options_ui, output_options_server
from gcode_web.operation.display_names import get_display_name, get_type
from gcode_web.operation.unique_operation import UniqueOperation

from conversational_gcode.options.Options import Options
from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.GcodeGenerator import GcodeGenerator

from conversational_gcode.operations.pocket.CircularPocket import CircularPocket
from conversational_gcode.operations.pocket.RectangularPocket import RectangularPocket
from conversational_gcode.operations.profile.CircularProfile import CircularProfile
from conversational_gcode.operations.profile.RectangularProfile import RectangularProfile
from conversational_gcode.operations.Drill import Drill

from conversational_gcode.gcodes.GCodes import GCode


operations = [
    CircularPocket,
    RectangularPocket,
    CircularProfile,
    RectangularProfile,
    Drill
]


def _create_new_job():
    return GCodeConfig()


@module.ui
def sidebar_ui():
    return ui.sidebar(
        ui.input_action_button(id='clear_btn', label='Clear'),
        ui.input_action_button(id='new_job_btn', label='New Job'),
        ui.input_select(
            id='operation_type',
            label='Operation',
            choices=list([get_display_name(clazz) for clazz in operations])
        ),
        ui.input_action_button(id='new_operation_btn', label='Add Operation'),
        ui.accordion(
            ui.accordion_panel(
                'Output Options',
                output_options_ui(id='output_options')
            ),
            open=False
        ),
        ui.input_action_button(id='generate_gcode_btn', label='Generate GCode'),
        # ui.download_button(id='save_jobs_btn', label='Save Jobs'),
        # ui.input_action_button(id='load_jobs_btn', label='Load Jobs')
    )


@module.server
def sidebar_server(
        input: Inputs,
        output: Outputs,
        session: Session,
        selected_job_id: reactive.Calc,
        job_configurations: reactive.Value[list[GCodeConfig]],
        added_operation: reactive.Value[tuple[GCodeConfig, object]]):
    output_options = OutputOptions()
    output_options_server(id='output_options', config=output_options)

    gcode_files = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.new_job_btn)
    def _add_job():
        new_job = _create_new_job()
        # TODO: Ideally this would update the list, then simply add the tab. That functionality is not yet available in Shiny
        job_configurations.set([*job_configurations.get(), new_job])

    @reactive.Effect
    @reactive.event(input.new_operation_btn)
    def _add_operation():
        job_id = selected_job_id()
        if job_id is None:
            print("Selected tab not found.")
            return

        job = next(job_config for job_config in job_configurations.get() if job_config.id == job_id)

        operation = UniqueOperation(get_type(input.operation_type())())
        job.operations.append(operation)

        added_operation.set((job, operation))

    @reactive.Effect
    @reactive.event(input.generate_gcode_btn)
    def _generate():
        gcode_jobs = []
        index = 0
        for job in job_configurations():
            options = Options(job.tool_config, job.job_config, output_options)
            generator = GcodeGenerator(options)
            for op in job.operations:
                generator.add_operation(op.operation)

            try:
                commands = [command.format(output_options) for command in generator.generate()]
            except Exception as exptn:
                traceback.print_exception(*sys.exc_info())
                commands = [GCode('Something went wrong. Please contact the app administrator for help.').format(output_options)]
            gcode_jobs.append(GcodeFile(job.name, commands))
            index += 1
        gcode_files.set(gcode_jobs)

    @reactive.Effect
    @reactive.event(input.clear_btn)
    def _clear():
        job_configurations.set([])
        gcode_files.set([])

    return gcode_files
