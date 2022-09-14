# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '10_standard',
        'name': 'exportTxtCmdLst',
        'index': 100,
        'icon': '<i class="bi bi-save"></i>',
        'tooltip': 'Export TextCommands List'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        ui: adsk.core.UserInterface = app.userInterface

        path = get_Filepath(f'txt_{app.version}.txt')
        if len(path) < 1:
            return

        txtCmd = u'TextCommands.List /Hidden'
        data = app.executeTextCommand(txtCmd)
        data = data.replace('\r', '')

        with open(path, mode="w", encoding='utf-8') as f:
            f.write(txtCmd + '\n')
            f.write(data)

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))


# get save file path
def get_Filepath(initialFilename='') -> str:
    ui: adsk.core.UserInterface = adsk.core.Application.get().userInterface

    dlg: adsk.core.FileDialog = ui.createFileDialog()
    dlg.title = 'Save File'
    dlg.isMultiSelectEnabled = False
    dlg.filter = 'Txt(*.txt)'
    if len(initialFilename) > 0:
        dlg.initialFilename = initialFilename

    if dlg.showSave() != adsk.core.DialogResults.DialogOK:
        return ''

    return dlg.filename