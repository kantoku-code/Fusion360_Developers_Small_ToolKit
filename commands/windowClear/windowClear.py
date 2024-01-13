# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'windowClear',
        'index': -1,
        'icon': '<i class="bi bi-eraser-fill"></i>',
        'tooltip': 'Window Clear'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        res = app.executeTextCommand(u'window.Clear')
        app.log(res)
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))