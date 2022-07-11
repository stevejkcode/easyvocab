# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_uiOlooMA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from aqt.qt import *


class MainDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Generate Foreign Language Cards")
        Dialog.resize(531, 525)

        Dialog.setWindowTitle('Generate Foreign Language Cards')

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(180, 490, 166, 25))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(9, 9, 511, 471))

        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setValue(2)

        self.gridLayout.addWidget(self.spinBox, 5, 0, 1, 1)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 3, 0, 1, 3)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout.addWidget(self.radioButton, 4, 0, 1, 3)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 1, 1, 4)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 2)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 3, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(328, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 2, 0, 1, 5)

        self.horizontalSpacer_3 = QSpacerItem(178, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 4, 3, 1, 2)

        self.horizontalSpacer = QSpacerItem(228, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 2, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(108, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 4, 1, 1)

        self.textEdit = QTextEdit(self.groupBox)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 5)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Generate Foreign Language Cards", None))
        self.groupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.spinBox.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The default number of translations to use on the reverse side of each card</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Choose or create a deck to import words into</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.comboBox.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.comboBox.setCurrentText("")
        self.comboBox.setPlaceholderText(QCoreApplication.translate("Dialog", u"Deck", None))
#if QT_CONFIG(tooltip)
        self.radioButton.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Create reverse vocab cards in addition to normal ones.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Create reverse cards", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Default number of translations", None))
#if QT_CONFIG(tooltip)
        self.pushButton.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Import words file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Select file...", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Deck", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter words...", None))
    # retranslateUi

