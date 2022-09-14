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
        'name': 'openInstallPostFolder',
        'index': 20,
        'icon': '<i class="bi bi-gear-fill"></i>',
        'tooltip': 'Open InstallPost Folder'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        tmpPath = getPath('cloudCacheDirectory')
        if not tmpPath:
            return

        postPath = pathlib.Path(tmpPath).parent / 'CAM' / 'cache' / 'posts'
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
