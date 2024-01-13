# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

_cmdLog_handler = None
_panel = False
_handlers = []
DEBUG = True

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


def get_active_tab() -> adsk.core.ToolbarTab:
    app: adsk.core.Application = adsk.core.Application.get()
    ui: adsk.core.UserInterface = app.userInterface

    tabs: list[adsk.core.ToolbarTab] = [tb for tb in ui.allToolbarTabs 
        if all([tb.isActive, tb.isVisible])]
    
    if len(tabs) < 1:
        return None
    else:
        return tabs[0]


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

                # tab
                tab: adsk.core.ToolbarTab = get_active_tab()
                if not tab: return

                # panel
                panel: adsk.core.ToolbarPanel = None
                for panel in tab.toolbarPanels:

                    control: adsk.core.ToolbarControl = panel.controls.itemById(
                        args.commandId
                    )
                    if control:
                        app.log(
                            ' Workspace_ID:{}\n  Tab_ID:{}\n  Panel_ID:{}'.format(
                                ws.id, tab.id, panel.id
                            )
                        )
                        break
                    else:
                        dropdowns = [c for c in panel.controls
                            if c.classType() == adsk.core.DropDownControl.classType()
                        ]

                        dropdownControl: adsk.core.DropDownControl = None
                        for dropdownControl in dropdowns:

                            control: adsk.core.ToolbarControl = dropdownControl.controls.itemById(
                                args.commandId
                            )
                            if not control: continue

                            app.log(
                                ' Workspace_ID:{}\n  Tab_ID:{}\n  Panel_ID:{}'.format(
                                    ws.id, tab.id, panel.id
                                )
                            )
                            break

                # app.log(
                #     ' Workspace_ID:{}\n  Tab_ID:{}\n  Panel_ID: **unknown**'.format(
                #         ws.id, tab.id
                #     )
                # )

        except:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def dump(s):
    if DEBUG:
        print(s)