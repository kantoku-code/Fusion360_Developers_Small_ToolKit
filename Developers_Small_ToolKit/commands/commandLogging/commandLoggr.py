# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

_cmdLog_handler = None
_panel = False
_handlers = []

def entry() -> dict:
    return {
        'category': '30_commandLogging',
        'name': 'Cmd Log',
        'index': -1,
        'icon': '',
        'tooltip': 'Command Logging',
        'btn_type': 'switch_check',
        'check_name': 'Panel',
        'check_tooltip': 'Panel Informatione',
    }


def run(context):
    pass

def changeSwitchCheckValue(sw_value, ch_value) -> bool:
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        ui: adsk.core.UserInterface = app.userInterface

        global _cmdLog_handler, _handlers, _panel
        _panel = ch_value
        removeFG = False
        if sw_value:
            if not _cmdLog_handler:
                _cmdLog_handler = CommandStartingHandler()

            app.log('-- start command log --')
            ui.commandStarting.add(_cmdLog_handler)
            _handlers.append(_cmdLog_handler)
            removeFG = True
        else:
            removeEvent()

        return removeFG

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))

def removeEvent():
    app: adsk.core.Application = adsk.core.Application.get()
    ui: adsk.core.UserInterface = app.userInterface

    global _cmdLog_handler, _handlers, _panel
    app.log('-- stop command log --')
    ui.commandStarting.remove(_cmdLog_handler)
    _handlers.remove(_cmdLog_handler)

class CommandStartingHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        app: adsk.core.Application = adsk.core.Application.get()
        ui: adsk.core.UserInterface = app.userInterface
        try:
            # command
            cmdDefs: adsk.core.CommandDefinitions = ui.commandDefinitions

            cmdId: str = args.commandId
            cmdDef: adsk.core.CommandDefinition = cmdDefs.itemById(cmdId)
            cmdName: str = cmdDef.name if cmdDef else '(unknown)'

            app.log('{} : {}'.format(cmdName, cmdId))

            # panel
            global _panel
            if _panel:
                # workspace
                try:
                    ws: adsk.core.Workspace = ui.activeWorkspace
                except:
                    return

                # Toolbar panel
                panelId: str = ''
                try:
                    actEditObj = adsk.fusion.Sketch.cast(app.activeEditObject)
                    if actEditObj:
                        # sketch
                        tpIds = [
                            'SketchCreatePanel',
                            'SketchModifyPanel',
                            'SketchConstraintsPanel',
                            # 'PCB3DSketchCreatePanel'
                        ]

                        panels = ui.allToolbarPanels
                        tpLst = [panels.itemById(tpId) for tpId in tpIds]
                    else:
                        # other Design
                        tpLst = ui.toolbarPanelsByProductType(ws.productType)
                except:
                    # other non Design
                    tpLst = ui.toolbarPanelsByProductType(ws.productType)

                for tp in tpLst:
                    tc: adsk.core.ToolbarControl = tp.controls.itemById(cmdId)
                    if tc:
                        panelId = tp.id
                        break

                    # DropDownControl
                    for dd in tp.controls:
                        if adsk.core.DropDownControl.cast(dd):
                            tc = dd.controls.itemById(cmdId)
                            if tc:
                                panelId = tp.id
                                break

                # Toolbar tab
                tabId = ''
                if len(panelId) < 1:
                    panelId = tabId = '(unknown)'
                else:
                    ttLst = ui.toolbarTabsByProductType(ws.productType)
                    for tt in ttLst:
                        try:
                            tp = tt.toolbarPanels.itemById(panelId)
                        except:
                            continue

                        if tp:
                            tabId = tt.id
                            break

                    if len(tabId) < 1:
                        tabId = '(unknown)'

                app.log(' Workspace_ID:{}\n  Tab_ID:{}\n  Panel_ID:{}'.format(
                    ws.id, tabId, panelId))

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))