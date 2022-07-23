# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# Internal imports

from .src.ui import main_dialog


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def open_main_dialog() -> None:
    # Create and show the input cards dialog
    dialog = QDialog()
    dialog.ui = main_dialog.MainDialog()
    dialog.ui.setupUi(dialog)

    # Trigger the dialog
    dialog.exec_()


# create a new menu item, "Generate Foreign Language Cards"
action = QAction("Generate Foreign Language Cards", mw)
# set it to call open_main_dialog when it's clicked
qconnect(action.triggered, open_main_dialog)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
