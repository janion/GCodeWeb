from shiny import Inputs, Outputs, Session, ui, module, render, reactive

from gcode_web.job_config_tab import job_config_tab_ui, job_config_tab_server


def _create_jobs_navs(jobs: list):
    navs = []
    index = 0
    for job in jobs:
        navs.append(job_config_tab_ui(id=f'job_{job.id}', job=job))
        index += 1

    return ui.navset_tab(
                *navs,
                id='config_tabs'
            )


@module.ui
def config_panel_ui():
    return ui.output_ui(id='panel')


@module.server
def config_panel_server(input: Inputs, output: Outputs, session: Session, job_configurations, invalidated_job):
    @output
    @render.ui
    def panel():
        jobs = job_configurations.get()
        return _create_jobs_navs(jobs)

    # Reactive value so that individual jobs can react to other job names changing
    job_names = reactive.Value([])
    # Reactive value to allow for manual triggering of job name recalculation
    recalculate_job_names = reactive.Value(False)

    @reactive.Effect
    @reactive.event(job_configurations)
    def calculate_job_names_on_jobs_change():
        """Recalculate job names when job list changes"""
        job_names.set([job.job_config.name for job in job_configurations.get()])

    @reactive.Effect
    @reactive.event(recalculate_job_names)
    def calculate_job_names_manually():
        """Recalculate job names when manual trigger reactive value set to True"""
        if recalculate_job_names.get():
            recalculate_job_names.set(False)
            job_names.set([job.job_config.name for job in job_configurations.get()])

    @reactive.Effect
    @reactive.event(job_configurations)
    def _install_servers():
        jobs = job_configurations.get()
        last_job_id = None
        for job in jobs:
            job_config_tab_server(
                id=f'job_{job.id}',
                job=job,
                job_names=job_names,
                recalculate_job_names=recalculate_job_names,
                invalidated_job=invalidated_job
            )
            last_job_id = job.id

        # Select the final tab
        if last_job_id is not None:
            # TODO this is a bodge, but it kinda works for now
            ui.update_navs(id='config_tabs', selected=f'<div id="config_panel-job_{last_job_id}-title" class="shiny-text-output"></div>')

    return input.config_tabs
