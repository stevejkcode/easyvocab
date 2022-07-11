# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

from . import main_dialog

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    # # get the number of cards in the current collection, which is stored in
    # # the main window
    # cardCount = mw.col.cardCount()
    # # show a message box
    # showInfo("Card count: %d" % cardCount)

    # Create and show the input cards dialog
    # dialog = QDialog()
    # dialog.ui = main_dialog.MainDialog()
    # dialog.ui.setupUi(dialog)
    
    # dialog.exec_()

    # test select file code
    fileSelector = QFileDialog()
    fileSelector.setFileMode(QFileDialog.ExistingFile)
    fileSelector.setAcceptMode(QFileDialog.AcceptOpen)
    fileSelector.setNameFilter("Text files (*.txt)")

    # widget = QWidget()
    # fileName = QFileDialog.getOpenFileName(widget, 'Open file', '~', 'Image files (*.jpg *.gif)')

    if fileSelector.exec_():
        fileName = fileSelector.selectedFiles()
        showInfo(f"file selected {fileName[0]}")


# create a new menu item, "test"
action = QAction("Generate Foreign Language Cards", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


class InputCardsDialog(QDialog):
    # Needed widgets:
        # Large input box for cards
        # File selector to populate input box directly
        # Target deck 
        # Source language
        # Target language
        # Text to speech checkbox
        # Generate reverse cards checkbox
        # Submit button
        # Cancel button

    def __init__(self, parent=None):
        super().__init__(parent)

        layoutWidget = QWidget()
        layoutWidget.setObjectName("layoutWidget")

        globalLayout = QVBoxLayout()
        dlgLayout = QVBoxLayout(layoutWidget)
        formLayout = QFormLayout()

        nameLineEdit = QLineEdit()
        nameLineEdit.setFixedHeight(100)
        formLayout.addRow('Name:', nameLineEdit)
        formLayout.addRow('Age:', QLineEdit())
        formLayout.addRow('Job:', QLineEdit())
        formLayout.addRow('Hobbies:', QLineEdit())

        dlgLayout.addLayout(formLayout)

        scrollArea = QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        scrollArea.setObjectName("scrollArea")
        scrollArea.setWidget(layoutWidget)


        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        globalLayout.addWidget(scrollArea)
        globalLayout.addWidget(btns)

        self.setLayout(globalLayout)