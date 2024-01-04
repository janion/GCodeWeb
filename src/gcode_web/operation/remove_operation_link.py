from shiny import Inputs, Outputs, Session, ui, module, reactive


@module.ui
def remove_operation_ui():
    # A button would be preferred, but that doesn't play nicely with accordion panels in the current version of shiny
    return ui.input_action_link(id='delete', label="✖", style='text-decoration: unset; color: unset;')


@module.server
def remove_operation_server(input: Inputs, output: Outputs, session: Session):
    return input.delete
