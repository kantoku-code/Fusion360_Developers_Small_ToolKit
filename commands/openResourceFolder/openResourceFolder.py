# fusion360 API python

import traceback
import adsk.core
import adsk.fusion
import subprocess
import os
import platform

def entry() -> dict:
    return {
        'category': '60_folders',
        'name': 'openResourceFolder',
        'index': 100,
        'icon': '<i class="bi bi-command"></i>',
        'tooltip': 'Open Active Command Resource Folder'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    ui: adsk.core.UserInterface = app.userInterface
    try:

        cmdDef = ui.commandDefinitions.itemById(ui.activeCommand)
        if cmdDef:
            try:
                path = cmdDef.resourceFolder
            except:
                return

        openFolder(path)

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))


def openFolder(path: str):
    app: adsk.core.Application = adsk.core.Application.get()
    app.log(str(path))
    try:
        if platform.system() == 'Windows':
            os.startfile(str(path))
        else:
            subprocess.check_call(["open", "--", str(path)])
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))