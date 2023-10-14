import shiny.experimental as x
from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.options.job_options import job_options_ui, job_options_server
from gcode_web.options.tool_options import tool_options_ui, tool_options_server


def _create_job_ui(job_name: str, job: GCodeConfig):
    names_and_uis = []
    index = 0

    names_and_uis.append((job.job_config.display_name, job_options_ui(id=f'{job_name}_{index}', config=job.job_config)))
    index += 1

    names_and_uis.append((job.tool_config.display_name, tool_options_ui(id=f'{job_name}_{index}', config=job.tool_config)))
    index += 1

    for config in job.operations:
        # Create operation UI
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

            job_options_server(id=f'job_name_{job_index}_{config_index}', config=job.job_config)
            config_index += 1

            tool_options_server(id=f'job_name_{job_index}_{config_index}', config=job.tool_config)
            config_index += 1

            for config in job.operations:
                # Create operation server
                config_index += 1
            job_index += 1

        # Select the final tab
        ui.update_navs(id='config_tabs', selected=f'job_name_{len(jobs) - 1}')
