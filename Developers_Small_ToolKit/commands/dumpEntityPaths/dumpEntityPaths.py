# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'dumpEntityPaths',
        'index': 30,
        'icon': '<i class="bi bi-pencil-fill"></i>',
        'tooltip': 'Dump Entity Paths'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        try:
            res = app.executeTextCommand(u'Selections.List')
            app.log(res)
        except:
            pass
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))