# fusion360 API python

import traceback
import adsk.core as core
import adsk.fusion as fusion

DIALOG_TITLE = "ReBoot Document"

def entry() -> dict:
    return {
        'category': '10_standard',
        'name': 'reboot_document',
        'index': 200,
        'icon': '<i class="bi bi-bootstrap-reboot"></i>',
        'tooltip': 'Reboot Document'
    }

def run(context):
    ui: core.UserInterface = None
    try:
        app: core.Application = core.Application.get()
        ui = app.userInterface

        reboot_doc()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def reboot_doc():
    app: core.Application = core.Application.get()
    ui: core.UserInterface = app.userInterface

    docs: core.Documents = app.documents
    doc: fusion.FusionDocument = app.activeDocument

    if not doc.isModified:
        show_message("Canceled due to no change.")
        return

    dataFile: core.DataFile = doc.dataFile

    if not dataFile:
        show_message("Abort because the document has never been saved.")
        return

    res: core.DialogResults = ui.messageBox(
        "Discard changes and reopen?",
        DIALOG_TITLE,
        core.MessageBoxButtonTypes.OKCancelButtonType,
        core.MessageBoxIconTypes.QuestionIconType,
    )
    if res != core.DialogResults.DialogOK: return

    doc.close(False)
    docs.open(dataFile)


def show_message(msg: str) -> None:
    app: core.Application = core.Application.get()
    ui: core.UserInterface = app.userInterface

    ui.messageBox(
        msg,
        DIALOG_TITLE,
        core.MessageBoxButtonTypes.OKButtonType,
        core.MessageBoxIconTypes.NoIconIconType,
    )