# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'dumpONK',
        'index': 100,
        'icon': '<i class="bi bi-inbox"></i>',
        'tooltip': 'Dump ONK'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        try:
            res = app.executeTextCommand(u'ObjectPaths.Onk')
            app.log(res)
        except:
            pass
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))