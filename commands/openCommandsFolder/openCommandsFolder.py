# fusion360 API python

import traceback
import adsk.core
import adsk.fusion
import pathlib
import json
import platform
import os
import subprocess

def entry() -> dict:
    return {
        'category': '60_folders',
        'name': 'openCommandsFolder',
        'index': 200,
        'icon': '<i class="bi bi-textarea"></i>',
        'tooltip': 'Open the folder to add the Commands'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:

        path = THIS_DIR = pathlib.Path(__file__).resolve().parent.parent
        openFolder(path)

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))


def getPath(key: str) -> str:
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        paths = json.loads(app.executeTextCommand(u'Paths.Get'))
        return paths[key]

    except:
        return None


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
