# fusion360 API python

import traceback
import adsk.core
import adsk.fusion
import json

def entry() -> dict:
    return {
        'category': '70_attrs',
        'name': 'dumpUserPrmAttrs',
        'index': 30,
        'icon': '<i class="bi bi-text-left"></i>',
        'tooltip': 'Dump UserParameter Attributes'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        prms: adsk.fusion.UserParameters = app.activeDocument.design.userParameters

        app.log('TextCommandWindow.Clear')
        app.log('-- Dump User UserParameter Attributes --')
        attr: adsk.core.Attribute
        prm: adsk.fusion.UserParameter
        for prm in prms:
            app.log(f'**PrmName:{prm.name}**')
            for groupName in prm.attributes.groupNames:
                group = prm.attributes.itemsByGroup(groupName)
                app.log(f'GroupName:{groupName}')
                for attr in group:
                    app.log(f'  Name:{attr.name}  ValueSize:{len(attr.value.encode())}')

                    dict = json.loads(attr.value)
                    for key in dict.keys():
                        app.log(f'    {key}:{dict[key]}')

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))