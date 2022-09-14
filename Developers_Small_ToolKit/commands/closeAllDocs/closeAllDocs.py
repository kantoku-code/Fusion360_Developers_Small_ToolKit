# fusion360 API python

import traceback
import adsk.core
import adsk.fusion

def entry() -> dict:
    return {
        'category': '10_standard',
        'name': 'closeAllDocs',
        'index': -1,
        'icon': '<i class="bi bi-door-closed"></i>',
        'tooltip': 'Close All Docs'
    }


def run(context):
    app: adsk.core.Application = adsk.core.Application.get()
    try:
        ui: adsk.core.UserInterface = app.userInterface

        def closeDocs(docs):
            for doc in docs[::-1]:
                try:
                    doc.close(False)
                except:
                    pass

        # *********

        closeDocs(
            [doc for doc in app.documents if not doc.isModified]
        )

        docs = [doc for doc in app.documents]
        msg = [
            f'The number of open documents is {len(docs)}.',
            'Would you like me to close them all without saving them?'
        ]

        if not ui.messageBox(
            '\n'.join(msg),
            '',
            adsk.core.MessageBoxButtonTypes.OKCancelButtonType,
            adsk.core.MessageBoxIconTypes.QuestionIconType
        ) == adsk.core.DialogResults.DialogOK:
            return

        closeDocs(docs)

    except:
        app.log('Failed:\n{}'.format(traceback.format_exc()))