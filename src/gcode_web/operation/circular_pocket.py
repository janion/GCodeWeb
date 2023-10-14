from shiny import Inputs, Outputs, Session, ui, module, reactive


@module.ui
def circular_pocket_ui():
    return ui.div()


@module.server
def circular_pocket_server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def operation():
        return []
