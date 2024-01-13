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
        'name': 'penUserDirectory',
        'index': 20,
        'icon': '<i class="bi bi-person-fill"></i>',
        'tooltip': 'Open User Directory'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:

        path = app.executeTextCommand(u'Paths.UserDirectory')
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