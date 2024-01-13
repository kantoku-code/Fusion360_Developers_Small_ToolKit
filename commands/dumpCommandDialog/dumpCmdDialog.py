# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'dumpCommandDialog',
        'index': 10,
        'icon': '<i class="bi bi-printer"></i>',
        'tooltip': 'Dump CommandDialog Info'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        res = app.executeTextCommand(u'Toolkit.cmdDialog')
        app.log(res)
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))