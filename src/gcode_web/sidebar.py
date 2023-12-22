from re import search

import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.output.gcode_file import GcodeFile
from gcode_web.options.output_options import output_options_ui, output_options_server
from gcode_web.operation.display_names import get_display_name, get_type

from conversational_gcode.options.Options import Options
from conversational_gcode.options.OutputOptions import OutputOptions
from conversational_gcode.GcodeGenerator import GcodeGenerator
from conversational_gcode.operations.CircularPocket import CircularPocket


operations = [
    CircularPocket
]


def _create_new_job():
    return GCodeConfig()


@module.ui
def sidebar_ui():
    return x.ui.sidebar(
        ui.input_action_button(id='clear_btn', label='Clear'),
        ui.input_action_button(id='new_job_btn', label='New Job'),
        ui.hr(),
        ui.input_select(
            id='operation_type',
            label='Operation',
            choices=list([get_display_name(clazz) for clazz in operations])
        ),
        ui.input_action_button(id='new_operation_btn', label='Add Operation'),
        ui.hr(),
        x.ui.accordion_panel(
            'Output Options',
            output_options_ui(id='output_options')
        ),
        ui.input_action_button(id='generate_gcode_btn', label='Generate GCode'),
        # ui.download_button(id='save_jobs_btn', label='Save Jobs'),
        # ui.input_action_button(id='load_jobs_btn', label='Load Jobs')
    )


@module.server
def sidebar_server(input: Inputs, output: Outputs, session: Session, config_tabs, job_configurations):
    output_options = OutputOptions()
    output_options_server(id='output_options', config=output_options)

    @reactive.Effect
    @reactive.event(input.new_job_btn)
    def _add_job():
        job_configurations.set(job_configurations.get() + [_create_new_job()])

    @reactive.Effect
    @reactive.event(input.new_operation_btn)
    def _add_operation():
        operation = get_type(input.operation_type())()

        # TODO This should not be hard-coded
        match = search('config_panel-job_([0-9]+)-title', config_tabs())
        job_id = int(match.group(1))
        job_index = job_id

        job = job_configurations.get()[job_index]
        job.operations.append(operation)

        tmp = job_configurations.get()
        job_configurations.set([])
        job_configurations.set(tmp)

    gcode_files = reactive.Value([])

    @reactive.Effect
    @reactive.event(input.generate_gcode_btn)
    def _generate():
        gcode_jobs = []
        index = 0
        for job in job_configurations():
            options = Options(job.tool_config, job.job_config, output_options)
            generator = GcodeGenerator(options)
            for op in job.operations:
                generator.add_operation(op)

            commands = [command.format(output_options) for command in generator.generate()]
            gcode_jobs.append(GcodeFile(job.job_config.name, commands))
            index += 1
        gcode_files.set(gcode_jobs)

    @reactive.Effect
    @reactive.event(input.clear_btn)
    def _clear():
        job_configurations.set([])
        gcode_files.set([])

    return gcode_files
