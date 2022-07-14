import os
import sys

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))

# Internal imports
from .ui import main_dialog
from .main import generate_cards

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def openMainDialog() -> None:
    # Create and show the input cards dialog
    dialog = QDialog()
    dialog.ui = main_dialog.MainDialog()
    dialog.ui.setupUi(dialog)

    # Wire accept button to trigger generation process
    dialog.ui.buttonBox.accepted.connect(handle_accept(dialog))

    # Trigger the dialog
    dialog.exec_()

# Helper function to trigger the card generation process when the accept button is clicked
# Retrieves options from the UI and forwards them along with the list of words to the process 
def handle_accept(dialog):
    def _f():
        text       = dialog.ui.textEdit.toPlainText()
        collection = mw.col

        options = {}

        # Get the target deck from the dialog
        deck = dialog.ui.comboBox.currentData()

        # Get the language settings from the dialog
        src  = dialog.ui.comboBox_2.currentData()
        dest = dialog.ui.comboBox_3.currentData()
        options['language'] = {'src': src, 'dest': dest}

        # Get the reverse setting from the dialog
        reverse = dialog.ui.radioButton.isChecked()
        options['reverse'] = reverse

        # Get the number of translations to include
        translations = dialog.ui.spinBox.value()
        options['translations'] = translations

        generate_cards(collection, deck, text, options, dialog.close)
    
    return _f


# create a new menu item, "test"
action = QAction("Generate Foreign Language Cards", mw)
# set it to call openMainDialog when it's clicked
qconnect(action.triggered, openMainDialog)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
