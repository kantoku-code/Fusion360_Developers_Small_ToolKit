# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '60_folders',
        'name': 'openCache',
        'index': 10,
        'icon': '<i class="bi bi-bag"></i>',
        'tooltip': 'Open Cache Folder'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        app.executeTextCommand(u'Cache.open')
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))