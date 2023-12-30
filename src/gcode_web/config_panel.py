from re import search

from shiny import Inputs, Outputs, Session, ui, reactive, render, module

from gcode_web.output.gcode_config import GCodeConfig
from gcode_web.job_config_tab import job_tab_ui, job_tab_server


@module.ui
def jobs_panel_ui():
    return ui.output_ui(id='tabs')


@module.server
def jobs_panel_server(input: Inputs, output: Outputs, session: Session, jobs: reactive.Value[list[GCodeConfig]], modified_job_id: reactive.Value[int]):
    job_names = reactive.Value([])
    recalculate_job_names = reactive.Value(False)

    @reactive.Effect
    @reactive.event(recalculate_job_names)
    def _manually_recalculate_job_names():
        if recalculate_job_names.get():
            job_names.set([job.job_config.name for job in jobs.get()])
            recalculate_job_names.set(False)

    @output
    @render.ui
    def tabs():
        navs = []
        last_job_id = 0
        for job in jobs.get():
            navs.append(job_tab_ui(id=f'tab_{job.id}', job=job))
            last_job_id = job.id
        return ui.navset_tab(
            *navs,
            id='tabs',
            # Select final tab
            selected=f'tab_{last_job_id}'
        )

    @reactive.Effect
    def _install_servers():
        for job in jobs.get():
            job_name = job_tab_server(id=f'tab_{job.id}', job=job, job_names=job_names)

            @reactive.Effect
            @reactive.event(job_name)
            def _job_name_changed():
                recalculate_job_names.set(True)

    @reactive.Effect
    def _select_tab():
        ui.update_navs(id='tabs', selected=f'tab_{modified_job_id.get()}')
        modified_job_id.set(None)

    @reactive.Calc
    def selected_job_id():
        match = search('tab_([0-9]+)', input.tabs())
        if match is None:
            return None
        return int(match.group(1))

    return selected_job_id
