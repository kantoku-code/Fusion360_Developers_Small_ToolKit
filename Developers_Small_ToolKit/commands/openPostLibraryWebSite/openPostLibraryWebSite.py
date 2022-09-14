# fusion360 API python

import traceback
import adsk.core
import adsk.fusion
import webbrowser

def entry() -> dict:
    return {
        'category': '20_manufacture',
        'name': 'openPostLibraryWebSite',
        'index': 100,
        'icon': '<i class="bi bi-arrow-up-right-square"></i>',
        'tooltip': 'Open Post Library WebSite'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        webbrowser.open('https://cam.autodesk.com/hsmposts?')

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))