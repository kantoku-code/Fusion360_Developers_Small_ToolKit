# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '70_attrs',
        'name': 'removeDocAttrs',
        'index': 20,
        'icon': '<i class="bi bi-file-earmark-x"></i>',
        'tooltip': 'Remove Document Attributes'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:

        doc: adsk.fusion.FusionDocument = app.activeDocument
        attrs: adsk.core.Attributes = doc.attributes

        # Query
        ui: adsk.core.UserInterface = app.userInterface
        msg = f'There are {attrs.count} attributes. Do you want to delete them all?'
        res = ui.messageBox(
            msg,
            '',
            adsk.core.MessageBoxButtonTypes.YesNoButtonType,
            adsk.core.MessageBoxIconTypes.WarningIconType
        )
        if res == adsk.core.DialogResults.DialogNo:
            return

        app.log('TextCommandWindow.Clear')
        app.log('-- Remove Document Attributes --')
        app.log(f'before count:{attrs.count}')
        attr: adsk.core.Attribute
        for gpName in attrs.groupNames:
            app.log(f'GroupName : {gpName}')
            for attr in attrs.itemsByGroup(gpName):
                attr.deleteMe()
        app.log(f'after count:{attrs.count}')

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))