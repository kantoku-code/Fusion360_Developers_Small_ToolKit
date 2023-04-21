# fusion360 API python

import traceback
import adsk.core as core
import adsk.cam as cam
import pathlib
import os
import platform
import subprocess
import time

THIS_DIR = pathlib.Path(__file__).resolve().parent

def entry() -> dict:
    return {
        'category': '20_manufacture',
        'name': 'dumpCAMParameters',
        'index': 1000,
        'icon': '<i class="bi bi-text-left"></i>',
        'tooltip': 'Dump CAMParameters'
    }


def run(context):
    app: core.Application = core.Application.get()
    try:
        ui: core.UserInterface = app.userInterface

        if app.activeProduct.objectType != cam.CAM.classType():
            ui.messageBox('The Manufacturing workspace must be active.')
            return

        sels: core.Selections = ui.activeSelections
        if sels.count < 1:
            ui.messageBox('Please select elements in advance.')
            return

        entity = sels.item(0).entity
        if not hasattr(entity, 'parameters'):
            return

        info = get_parameters(entity.parameters, False)
        if len(info) < 1:
            return

        show_info(info)

        # app.log(app.executeTextCommand(u'window.Clear'))
        # app.log(info)

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))


def show_info(txt: str) -> None:

    path = get_unique_path()
    with open(path, mode='w') as f:
        f.write(txt)

    if platform.system() == 'Windows':  
        os.startfile(path)
    else:
        subprocess.check_call(["open", "--", path])

    time.sleep(0.5)

    os.remove(path)

def get_unique_path() -> str:

    fileName = 'Dump CAM Parameters.txt'

    path: pathlib.Path = pathlib.Path(THIS_DIR) / fileName
    if not path.exists():
        return str(path)

    stem = path.stem
    count = 1
    while True:
        path = path.with_stem(f'{stem}_{count}')
        if not path.exists():
            return str(path)
        count += 1


def get_parameters(
    params: cam.CAMParameters,
    showOnlyEditable: bool
) -> str:

    try:
        paramList = []
        param: cam.CAMParameter
        for param in params:
            if param.isEditable:
                i = 1

            # Only write out this parameter if it's editable or if the showOnlyEditable flag is False.
            if param.isEditable or (not param.isEditable and not showOnlyEditable) :
                result = ''

                # Display the property values.
                result += f'name: {param.name}\n'
                result += f'    title: {param.title}\n'
                result += f'    expression: "{param.expression}"\n'
                result += f'    isEditable: {param.isEditable}\n'
                result += f'    isEnabled: {param.isEnabled}\n'

                # Attempt to get the value of the parameter. This does fail in
                # some cases.
                value = None
                try:
                    value = param.value
                except:
                    result += f'    ** Failed to get value type.\n'

                # Create information for each specific value type.
                if value:
                    if value.objectType == cam.FloatParameterValue.classType():
                        floatVal: cam.FloatParameterValue = value
                        result += f'    FloatParameterValue\n'
                        result += f'        value: {floatVal.value}\n'
                    elif value.objectType == cam.ChoiceParameterValue.classType():
                        choiceVal: cam.ChoiceParameterValue = value
                        result += f'    ChoiceParameterValue\n'
                        result += f'        value: {choiceVal.value}\n'
                        result += f'        choices:\n'
                        (_, names, values) = choiceVal.getChoices()
                        for i in range(len(names)):
                            result += f'            name: {names[i]}, value: {values[i]}\n'
                    elif value.objectType == cam.StringParameterValue.classType():
                        stringVal: cam.StringParameterValue = value
                        result += f'    StringParameterValue\n'
                        result += f'        value: {stringVal.value}\n'
                    elif value.objectType == cam.BooleanParameterValue.classType():
                        boolVal: cam.BooleanParameterValue = value
                        result += f'    FloatParameterValue\n'
                        result += f'        value: {boolVal.value}\n'
                    elif value.objectType == cam.IntegerParameterValue.classType():
                        intVal: cam.IntegerParameterValue = value
                        result += f'    FloatParameterValue\n'
                        result += f'        value: {intVal.value}\n'
                    elif value.objectType == cam.CadObjectParameterValue.classType():
                        cadObjectVal: cam.CadObjectParameterValue = value
                        result += f'    CadObjectParameterValue\n'
                        if len(cadObjectVal.value) == 0:                       
                            result += f'        value: Empty\n'
                        else:
                            result += f'        value:\n'
                            result += printGeometry(cadObjectVal.value, '            ')
                    elif value.objectType == cam.CadContours2dParameterValue.classType():
                        cadContourVal: cam.CadContours2dParameterValue = value
                        result += f'    CadContours2dParameterValue\n'
                        curveSelections = cadContourVal.getCurveSelections()
                        if curveSelections.count == 0:                       
                            result += f'        value: Empty\n'
                        else:
                            for i in range( len(curveSelections)):                               
                                if curveSelections[i].objectType == cam.PocketSelection.classType():
                                    pocketSel: cam.PocketSelection = curveSelections[i]
                                    result += f'        Curve Selection {i+1}: PocketSelection\n'
                                    result += f'            extensionMethod: {pocketSel.extensionMethod}\n'
                                    result += f'            isSelectingSamePlaneFaces: {pocketSel.isSelectingSamePlaneFaces}\n'
                                    result += f'            inputGeometry:\n'
                                    result += printGeometry(pocketSel.inputGeometry, '                ')
                                    result += f'            value:\n'
                                    result += printGeometry(pocketSel.inputGeometry, '                ')
                                elif curveSelections[i].objectType == cam.ChainSelection.classType():
                                    chainSel: cam.ChainSelection = curveSelections[i]
                                    result += f'        Curve Selection {i+1}: ChainSelection\n'
                                    result += f'            startExtensionLength: {chainSel.startExtensionLength}\n'
                                    result += f'            endExtensionLength: {chainSel.endExtensionLength}\n'
                                    result += f'            extensionMethod: {chainSel.extensionMethod}\n'
                                    result += f'            isOpen: {chainSel.isOpen}\n'
                                    result += f'            isOpenAllowed: {chainSel.isOpenAllowed}\n'
                                    result += f'            endExtensionLength: {chainSel.endExtensionLength}\n'
                                    result += f'            isReverted: {chainSel.isReverted}\n'
                                    result += f'            extensionType: {chainSel.extensionType}\n'
                                    result += f'            isReverted: {chainSel.isReverted}\n'
                                    result += f'            inputGeometry:\n'
                                    result += printGeometry(chainSel.inputGeometry, '                ')
                                    result += f'            value:\n'
                                    result += printGeometry(chainSel.inputGeometry, '                ')
                                elif curveSelections[i].objectType == cam.SilhouetteSelection.classType():
                                    silSel: cam.SilhouetteSelection = curveSelections[i]
                                    result += f'        Curve Selection {i+1}: SilhouetteSelection\n'
                                    result += f'            isSetupModelSelected: {silSel.isSetupModelSelected}\n'
                                    result += f'            loopType: {silSel.loopType}\n'
                                    result += f'            sideType: {silSel.sideType}\n'
                                    result += f'            inputGeometry:\n'
                                    result += printGeometry(silSel.inputGeometry, '                ')
                                    result += f'            value:\n'
                                    result += printGeometry(silSel.inputGeometry, '                ')
                                elif curveSelections[i].objectType == cam.FaceContourSelection.classType():
                                    faceSel: cam.FaceContourSelection = curveSelections[i]
                                    result += f'        Curve Selection {i+1}: FaceContourSelection\n'
                                    result += f'            loopType: {faceSel.loopType}\n'
                                    result += f'            isSelectingSamePlaneFaces: {faceSel.isSelectingSamePlaneFaces}\n'
                                    result += f'            sideType: {faceSel.sideType}\n'
                                    result += f'            inputGeometry:\n'
                                    result += printGeometry(faceSel.inputGeometry, '                ')
                                    result += f'            value:\n'
                                    result += printGeometry(faceSel.inputGeometry, '                ')

                paramList.append([param.name, f'\n{result}'])

        # Sort the list so it will be in alphabetical order.
        def sortFunc(paramItem):
            return paramItem[0]

        paramList.sort(key = sortFunc)

        # Convert it to a string.
        fullResult = ''
        for paramData in paramList:
            fullResult += paramData[1]

        return fullResult
    except:
        core.Application.get().userInterface.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        return '** Unexpected Failure getting parameter information.'


# Constructs a string representing a list of the geometry in the input list. 
def printGeometry(geomList: list, indent: str) -> str:
    result = ''
    for geom in geomList:
        aaa = ''
        aaa.split()
        typeName = geom.objectType.split('::')
        if result == '':
            result = f'{indent}{typeName[2]}'
        else:
            result += f'\n{indent}{typeName[2]}'

    return f'{result}\n'