# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '10_standard',
        'name': 'removeCG',
        'index': 10,
        'icon': '<i class="bi bi-eraser"></i>',
        'tooltip': 'Remove Custom Graphics'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        ui: adsk.core.UserInterface = app.userInterface

        des: adsk.fusion.Design = app.activeProduct
        cgs = [cmp.customGraphicsGroups for cmp in des.allComponents]
        cgs = [cg for cg in cgs if cg.count > 0]

        if len(cgs) < 1:
            return

        for cg in cgs:
            gps = [c for c in cg]
            gps.reverse()
            for gp in gps:
                gp.deleteMe()

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))