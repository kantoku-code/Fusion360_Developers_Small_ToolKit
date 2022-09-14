# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '70_attrs',
        'name': 'dumpDocAttrs',
        'index': 10,
        'icon': '<i class="bi bi-text-left"></i>',
        'tooltip': 'Dump Document Attributes'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        doc: adsk.fusion.FusionDocument = app.activeDocument
        attrs: adsk.core.Attributes = doc.attributes

        app.log('TextCommandWindow.Clear')
        app.log('-- Dump Document Attributes --')
        app.log(f'before count:{attrs.count}')
        attr: adsk.core.Attribute
        for gpName in attrs.groupNames:
            app.log(f'GroupName : {gpName}')
            for attr in attrs.itemsByGroup(gpName):
                app.log(f'  {attr.name}:{attr.value}')

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))