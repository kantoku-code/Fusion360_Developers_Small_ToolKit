# fusion360 API python

import traceback
import adsk.core
import adsk.fusion
import json

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'dumpRootIds',
        'index': 20,
        'icon': '<i class="bi bi-columns-gap"></i>',
        'tooltip': 'Dump RootIds'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        keys = json.loads(app.executeTextCommand(u'PAsset.RootIds'))

        msgLst = ['*** PAsset.RootIds_PEntity.ID ***']
        for key in keys:
            try:
                id = app.executeTextCommand(u'PEntity.ID {}'.format(key))
                msgLst.append(f'{key} : {id}')
            except:
                pass

        app.log('\n'.join(msgLst))

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))