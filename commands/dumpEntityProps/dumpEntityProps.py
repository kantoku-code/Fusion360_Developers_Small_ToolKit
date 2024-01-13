# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '50_txt_command',
        'name': 'dumpEntityProps',
        'index': 40,
        'icon': '<i class="bi bi-file-ppt"></i>',
        'tooltip': 'Dump Entity Props'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        sels: adsk.core.Selections = app.userInterface.activeSelections

        if sels.count < 1:
            app.log('non select')
            return

        res = app.executeTextCommand(u'Selections.List')
        paths = res.split()
        for path in paths:
            try:
                ids = path.split(':')
                app.log(f'PEntity.Properties __ Entity Id:{ids[-1]}')
                app.log(
                    app.executeTextCommand(
                        u'PEntity.Properties {}'.format(ids[-1])
                    )
                )
            except:
                pass
    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))