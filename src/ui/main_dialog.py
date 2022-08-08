# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialogUNXxYU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import os
import sys
import codecs

# import the main window object (mw) from aqt
from aqt import mw
from aqt.qt import *

from PyQt5 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "site-packages"))
import googletrans

from . import file_select_dialog, progress_dialog
from .. import util, generate


class MainDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(411, 550)
        Dialog.setAutoFillBackground(True)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(False)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(12, 12, 388, 527))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 4)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(188, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 3)
        spacerItem1 = QtWidgets.QSpacerItem(328, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 4)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 2, 1, 2)
        self.comboBox_3 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 4, 2, 1, 2)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(48, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 5, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 6, 2, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 7, 2, 1, 2)
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox.setProperty("value", 2)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 8, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 1, 1, 3)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout.addWidget(self.comboBox_2, 4, 0, 1, 2)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setStatusTip("")
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 5, 0, 1, 2)
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 6, 0, 1, 2)
        self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 7, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # perform final setup actions
        # note that these are actions outside of the ones auto generated by QtDesigner
        self.customSetup(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Generate Foreign Language Cards"))
        self.textEdit.setPlaceholderText(_translate("Dialog", "Enter words..."))
        self.pushButton.setToolTip(_translate("Dialog", "Import words file"))
        self.pushButton.setText(_translate("Dialog", "Select file..."))
        self.label_3.setText(_translate("Dialog", "Source Language"))
        self.label_4.setText(_translate("Dialog", "Target Language"))
        self.label.setText(_translate("Dialog", "Deck"))
        self.spinBox.setToolTip(_translate("Dialog", "The default number of translations to use on the reverse side of each card"))
        self.label_2.setText(_translate("Dialog", "Default number of translations"))
        self.comboBox.setToolTip(_translate("Dialog", "Choose which deck to import the generated cards into."))
        self.comboBox.setPlaceholderText(_translate("Dialog", "Deck"))
        self.checkBox.setToolTip(_translate("Dialog", "Create reverse vocab cards in addition to normal ones."))
        self.checkBox.setText(_translate("Dialog", "Create reverse cards"))
        self.checkBox_2.setToolTip(_translate("Dialog", "Enable text to speech. Google TTS will be used to generate audio for your cards."))
        self.checkBox_2.setText(_translate("Dialog", "Enable text-to-speech"))


    # Custom functions

    # Call the select file dialog, and handle opening and wiring in the file contents to the text box
    def populateFileText(self):
        filename = file_select_dialog.selectFile()

        if filename and filename != '':
                with codecs.open(filename, mode='r', encoding='utf-8') as file:
                    self.setBoxText(str(file.read()))

        return

    def create_progress_dialog(self) -> None:
        dialog = QDialog()
        dialog.ui = progress_dialog.ProgressDialog()
        dialog.ui.setupUi(dialog)

        return dialog

    def accept_dialog(self, Dialog):
        progress = self.create_progress_dialog()

        text       = self.textEdit.toPlainText()
        collection = mw.col

        options = {}

        # Get the target deck from the main dialog
        deck = self.comboBox.currentData()

        # Get the language settings from the combo boxes
        src  = self.comboBox_2.currentData()
        dest = self.comboBox_3.currentData()
        options['language'] = {'src': src, 'dest': dest}

        # Get the reverse setting from the main dialog
        reverse = self.checkBox.isChecked()
        options['reverse'] = reverse

        # Get the tts setting from the main dialog
        tts = self.checkBox_2.isChecked()
        options['tts'] = tts

        # Get the number of translations to include
        num_translations = self.spinBox.value()
        options['num_translations'] = num_translations

        generate.generate_cards(collection, deck, text, options, { 'main': Dialog, 'progress': progress })
        progress.exec_()

    # Custom dialog setup
    # Encapsulated in this function to limit the impact of UI changes / redesign
    def customSetup(self, Dialog):
        # connect select file button to the select file dialog
        self.pushButton.clicked.connect(self.populateFileText)

        # populate the deck list from anki into the combo box
        self.populateDecks(self.comboBox)

        # populate the set of source and target languages into their respective combo box
        self.populateLanguages(self.comboBox_2)
        self.populateLanguages(self.comboBox_3)

        # set the default target language to english
        index = self.comboBox_3.findData("en")
        self.comboBox_3.setCurrentIndex(index)

        # wire the accept button
        self.buttonBox.accepted.connect(util.wrap_nonary(self.accept_dialog)(Dialog))


    # Set the text within the main words entry text box
    def setBoxText(self, text):
        self.textEdit.setText(text)

    # Retrieve decks from anki and use them to populate the combo box
    def populateDecks(self, comboBox):
        decks = mw.col.decks.all_names_and_ids()

        index = 0

        for deck in decks:
            comboBox.addItem(deck.name, deck)

            if deck.name == 'Default':
                comboBox.setCurrentIndex(index)
            
            index += 1

    # Pull languages from googletrans and populate the combo boxes
    def populateLanguages(self, comboBox):
        # Add default empty entry for language dialog
        comboBox.addItem("", None)

        languages = googletrans.LANGUAGES

        for language_code, language_name in languages.items():
            comboBox.addItem(util.capitalize(language_name), language_code)