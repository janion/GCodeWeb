import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server
from gcode_web.operation.circular_pocket import circular_pocket_ui, circular_pocket_server
from gcode_web.operation.display_names import get_display_name

from conversational_gcode.operations.CircularPocket import CircularPocket


_output_options_display_name = 'Output Options'
_job_options_display_name = 'Job Options'
_tool_options_display_name = 'Tool Options'


def _create_job_ui(job_name: str, job: GCodeConfig):
    names_and_uis = []
    index = 0

    # TODO this should not be hard-coded
    names_and_uis.append((_job_options_display_name, job_options_ui(id=f'{job_name}_{index}', config=job.job_config)))
    index += 1

    # TODO this should not be hard-coded
    names_and_uis.append((_tool_options_display_name, tool_options_ui(id=f'{job_name}_{index}', config=job.tool_config)))
    index += 1

    for config in job.operations:
        if isinstance(config, CircularPocket):
            names_and_uis.append((get_display_name(type(config)), circular_pocket_ui(id=f'{job_name}_{index}', config=config)))
        index += 1

    return ui.nav(
        job_name,
        x.ui.accordion(
            *[x.ui.accordion_panel(name, each_ui) for name, each_ui in names_and_uis]
        )
    )


def _create_jobs_navs(jobs: list):
    navs = []
    index = 0
    for job in jobs:
        # TODO this should not be hard-coded
        navs.append(_create_job_ui(f'job_name_{index}', job))
        index += 1

    return ui.navset_tab(
                *navs,
                id='config_tabs'
            )


@module.ui
def config_panel_ui():
    return ui.output_ui(id='panel')


@module.server
def config_panel_server(input: Inputs, output: Outputs, session: Session, job_configurations):
    @output
    @render.ui
    def panel():
        jobs = job_configurations.get()
        return _create_jobs_navs(jobs)

    @reactive.Effect
    @reactive.event(job_configurations)
    def _install_servers():
        job_index = 0
        jobs = job_configurations.get()
        for job in jobs:
            config_index = 0

            # TODO this should not be hard-coded
            job_options_server(id=f'job_name_{job_index}_{config_index}', config=job.job_config)
            config_index += 1

            # TODO this should not be hard-coded
            tool_options_server(id=f'job_name_{job_index}_{config_index}', config=job.tool_config)
            config_index += 1

            for config in job.operations:
                if isinstance(config, CircularPocket):
                    # TODO this should not be hard-coded
                    circular_pocket_server(id=f'job_name_{job_index}_{config_index}', config=config)
                config_index += 1
            job_index += 1

        # Select the final tab
        # TODO this should not be hard-coded
        ui.update_navs(id='config_tabs', selected=f'job_name_{len(jobs) - 1}')

    return input.config_tabs
