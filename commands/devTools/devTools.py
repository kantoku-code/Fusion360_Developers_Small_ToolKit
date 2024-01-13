# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '40_dev_tools',
        'name': 'Dev Tools',
        'index': -1,
        'icon': '',
        'tooltip': 'Palette Developer Tools',
        'btn_type': 'switch',
    }


def run(context):
    pass


def changeValue(value):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        removeFG = False
        if value:
            app.log('-- start dev tools --')
            app.executeTextCommand(u'DevOptions.WebDeveloperExtras /on')
            removeFG = True
        else:
            removeEvent()

        return removeFG
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))

def removeEvent():
    app: adsk.core.Application = adsk.core.Application.get()

    app.log('-- stop dev tools --')
    app.executeTextCommand(u'DevOptions.WebDeveloperExtras /off')