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
        'category': '20_manufacture',
        'name': 'openCustomPostFolder',
        'index': 10,
        'icon': '<i class="bi bi-eraser"></i>',
        'tooltip': 'Open CustomPost Folder'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        ui: adsk.core.UserInterface = app.userInterface

        userPath = getPath('unbrandedUserDataDirectory')
        if not userPath:
            return

        postPath = pathlib.Path(userPath).parent / 'Fusion 360 CAM' / 'Posts'
        if not postPath.exists():
            return

        openFolder(postPath)

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
