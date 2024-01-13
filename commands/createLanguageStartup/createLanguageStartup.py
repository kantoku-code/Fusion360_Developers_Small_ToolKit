# fusion360 API python

import traceback
import adsk
import adsk.core as core
import adsk.fusion as fusion
import json
import pathlib
import os

THIS_DIR = pathlib.Path(__file__).resolve().parent
BASE_VBS_NAME = 'base.vbs'
FUSION_KEY = '@fusionpath'
OPTION_KEY = '@xmlpath'

def entry() -> dict:
    return {
        'category': '10_standard',
        'name': 'LanguageStartupScript',
        'index': 150,
        'icon': '<i class="bi bi-send"></i>',
        'tooltip': 'Create Language Startup Fusion360 Script'
    }

def run(context):
    ui = core.UserInterface.cast(None)
    try:
        app: core.Application = core.Application.get()
        ui = app.userInterface
        des: fusion.Design = app.activeProduct
        root: fusion.Component = des.rootComponent

        vbsCode = get_vbs_code()

        vbsPath = get_file_path()
        if len(vbsPath) < 1:
            return

        write_file(vbsPath, vbsCode)

        ui.messageBox(f'{vbsPath}\nを作成しました。')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def write_file(
    path: str,
    txt: str,
) -> None:

    with open(path, mode = "w", encoding="shift_jis") as f:
        f.write(txt)


def get_vbs_code() -> str:

    vbsPath = str(THIS_DIR / BASE_VBS_NAME)
    with open(vbsPath, encoding="shift_jis") as f:
        vbsCode = f.read()

    vbsCode = vbsCode.replace(
        FUSION_KEY, get_fusion_path()
        ).replace(
            OPTION_KEY, get_options_path()
        )

    return vbsCode


def get_fusion_path() -> str:

    app: core.Application = core.Application.get()

    pathDict = json.loads(app.executeTextCommand(u'paths.get'))
    # return str(pathlib.Path(pathDict["rootDirectory"]) / "Fusion360.exe")

    production = pathlib.Path(pathDict["rootDirectory"]).parent
    launchers = list(production.glob('*/FusionLauncher.exe'))
    launcher = min(launchers, key=lambda x: len(list(x.parent.iterdir())))

    return str(launcher)


def get_options_path() -> str:

    app: core.Application = core.Application.get()

    pathDict = json.loads(app.executeTextCommand(u'paths.get'))
    return str(pathlib.Path(pathDict["bootstrapOptionDirectory"]) / "NMachineSpecificOptions.xml")


def get_file_path() -> str:

    app: core.Application = core.Application.get()
    ui: core.UserInterface = app.userInterface

    ver = app.version.replace('.', '_')

    dlg: core.FileDialog = ui.createFileDialog()
    dlg.title = '起動スクリプトの作成'
    dlg.isMultiSelectEnabled = False
    dlg.filter = 'VBScript(*.vbs)'
    dlg.initialDirectory = os.path.expanduser('~/Desktop')
    dlg.initialFilename = f'Language Startup Fusion360 Ver{ver}'
    if dlg.showSave() != adsk.core.DialogResults.DialogOK :
        return ''

    return dlg.filename