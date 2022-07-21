# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# Internal imports
from .ui import main_dialog, progress_dialog
from .main import generate_cards

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def open_main_dialog() -> None:
    # Create and show the input cards dialog
    dialog = QDialog()
    dialog.ui = main_dialog.MainDialog()
    dialog.ui.setupUi(dialog)

    # Wire accept button to trigger generation process
    dialog.ui.buttonBox.accepted.connect(handle_accept(dialog))

    # Trigger the dialog
    dialog.exec_()

def create_progress_dialog() -> None:
    dialog = QDialog()
    dialog.ui = progress_dialog.ProgressDialog()
    dialog.ui.setupUi(dialog)

    return dialog

# Helper function to trigger the card generation process when the accept button is clicked
# Retrieves options from the UI and forwards them along with the list of words to the process 
def handle_accept(dialog_main):
    def _f():
        dialog_progress = create_progress_dialog()

        text       = dialog_main.ui.textEdit.toPlainText()
        collection = mw.col

        options = {}

        # Get the target deck from the dialog_main
        deck = dialog_main.ui.comboBox.currentData()

        # Get the language settings from the dialog_main
        src  = dialog_main.ui.comboBox_2.currentData()
        dest = dialog_main.ui.comboBox_3.currentData()
        options['language'] = {'src': src, 'dest': dest}

        # Get the reverse setting from the dialog_main
        reverse = dialog_main.ui.radioButton.isChecked()
        options['reverse'] = reverse

        # Get the number of translations to include
        translations = dialog_main.ui.spinBox.value()
        options['translations'] = translations

        generate_cards(collection, deck, text, options, dialog_main, dialog_progress)
        dialog_progress.exec_()
    
    return _f


# create a new menu item, "Generate Foreign Language Cards"
action = QAction("Generate Foreign Language Cards", mw)
# set it to call open_main_dialog when it's clicked
qconnect(action.triggered, open_main_dialog)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
