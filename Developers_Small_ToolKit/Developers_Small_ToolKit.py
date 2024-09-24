# Fusion360API Python Addin
import traceback
import adsk.core
import adsk.fusion
import adsk.drawing
import json
import sys
from .ModuleContainer import ModuleManager

DEBUG = False

_app: adsk.core.Application = None
_ui: adsk.core.UserInterface = None
_handlers = []
_startUp = []

_cmdInfo = {
    'id': 'KANTOKU_Developers_Small_ToolKit',
    'name': 'Developers Small ToolKit',
    'tooltip': 'Developers Small ToolKit',
    'resources': 'resources'
}

_paletteInfo = {
    'id': 'KANTOKU_Developers_Small_ToolKit_Palette',
    'name': 'Developers Small ToolKit',
    'htmlFileURL': './html/index.html',
    'isVisible': True,
    'showCloseButton': True,
    'isResizable': True,
    'width': 260,
    'height': 330,
    'useNewWebBrowser': True,
    'dockingState': adsk.core.PaletteDockingStates.PaletteDockStateRight
}

_module_Manager = None

class MyHTMLEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, htmlArgs: adsk.core.HTMLEventArgs):
        try:
            global _module_Manager
            if htmlArgs.action == 'DOMContentLoaded':
                # dom loaded
                htmlArgs.returnData = _module_Manager.getButtonInfo()
            elif htmlArgs.action == 'button_event':
                # click button
                btnArgs = json.loads(htmlArgs.data)
                _module_Manager.exec(btnArgs['id'])
            elif htmlArgs.action == 'switch_event':
                # change switch
                switctArgs = json.loads(htmlArgs.data)
                _module_Manager.changeValue(
                    switctArgs['id'],
                    switctArgs['value'],
                )
            elif htmlArgs.action == 'switch_check_event':
                # change switch & check
                switctArgs = json.loads(htmlArgs.data)
                _module_Manager.changeSwitchCheckValue(
                    switctArgs['id'],
                    switctArgs['sw_value'],
                    switctArgs['ch_value'],
                )
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ShowPaletteCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        CreatePalette()


class MyCloseEventHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            global _module_Manager
            del _module_Manager
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class ShowPaletteCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            global _handlers
            command = args.command
            onExecute = ShowPaletteCommandExecuteHandler()
            command.execute.add(onExecute)
            _handlers.append(onExecute)
        except:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


class MyWorkspaceActivatedHandler(adsk.core.WorkspaceEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            CreatePalette()

            global _startUp
            if len(_startUp) > 0:
                del _startUp[-1]
        except:
            adsk.core.Application.get().log('Failed:\n{}'.format(traceback.format_exc()))


def run(context):
    try:
        global _ui, _app
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        global _cmdInfo
        showPaletteCmdDef = _ui.commandDefinitions.itemById(_cmdInfo['id'])
        if showPaletteCmdDef:
            showPaletteCmdDef.deleteMe()

        showPaletteCmdDef = _ui.commandDefinitions.addButtonDefinition(
            _cmdInfo['id'],
            _cmdInfo['name'],
            _cmdInfo['tooltip'],
            _cmdInfo['resources']
        )

        global _module_Manager
        _module_Manager = ModuleManager()

        # panel
        global _handlers
        onCommandCreated = ShowPaletteCommandCreatedHandler()
        showPaletteCmdDef.commandCreated.add(onCommandCreated)
        _handlers.append(onCommandCreated)

        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cntrl = panel.controls.itemById('showPalette')
        if not cntrl:
            panel.controls.addCommand(showPaletteCmdDef)

        # start msg
        _app.log(f'Start addin: {_cmdInfo["name"]}')
        _app.log(f'  Fusion360 Ver{_app.version}')
        _app.log(f'  Python Ver{sys.version}')

        # showPaletteCmdDef.execute()

        # start up
        global _startUp
        onWorkspaceActivated = MyWorkspaceActivatedHandler()
        _ui.workspaceActivated.add(onWorkspaceActivated)
        _startUp.append(onWorkspaceActivated)

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        global _ui, _paletteInfo, _handlers
        palette = _ui.palettes.itemById(_paletteInfo['id'])
        if palette:
            palette.deleteMe()

        global _cmdInfo
        panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        cmd = panel.controls.itemById(_cmdInfo['id'])
        if cmd:
            cmd.deleteMe()
        cmdDef = _ui.commandDefinitions.itemById(_cmdInfo['id'])
        if cmdDef:
            cmdDef.deleteMe()

        dumpLog('-- stop dev tools --')
        _app.executeTextCommand(u'DevOptions.WebDeveloperExtras /off')

        _app.log(f'Stop addin: {_cmdInfo["name"]}')
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def CreatePalette():
    try:
        global _ui, _paletteInfo

        palette: adsk.core.Palette = _ui.palettes.itemById(_paletteInfo['id'])
        if palette:
            palette.deleteMe()

        palette: adsk.core.Palette = _ui.palettes.add(
            _paletteInfo['id'],
            _paletteInfo['name'],
            _paletteInfo['htmlFileURL'],
            _paletteInfo['isVisible'],
            _paletteInfo['showCloseButton'],
            _paletteInfo['isResizable'],
            _paletteInfo['width'],
            _paletteInfo['height'],
            _paletteInfo['useNewWebBrowser'],
        )

        if _paletteInfo['dockingState']:
            palette.dockingState = _paletteInfo['dockingState']
        else:
            palette.setPosition(1000, 500)

        global _handlers
        onHTMLEvent = MyHTMLEventHandler()
        palette.incomingFromHTML.add(onHTMLEvent)
        _handlers.append(onHTMLEvent)

        onClosed = MyCloseEventHandler()
        palette.closed.add(onClosed)
        _handlers.append(onClosed)

    except:
        _ui.messageBox(
            'Command executed failed: {}'.format(
                traceback.format_exc()
            )
        )


def dumpLog(msg):
    if DEBUG:
        adsk.core.Application.log(f'{msg}')