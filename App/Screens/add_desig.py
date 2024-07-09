# -*- coding: utf-8 -*-

##########################################################################
# Form generated from reading UI file 'add_desig.ui'
##
# Created by: Qt User Interface Compiler version 6.7.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##########################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)


class Ui_Desig(QWidget):
    def setupUi(self, UiDesig):
        if not UiDesig.objectName():
            UiDesig.setObjectName(u"UiDesig")
        UiDesig.resize(222, 254)
        self.verticalLayout_5 = QVBoxLayout(UiDesig)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_desig = QLabel(UiDesig)
        self.lbl_desig.setObjectName(u"lbl_desig")

        self.verticalLayout.addWidget(self.lbl_desig)

        self.en_desig = QLineEdit(UiDesig)
        self.en_desig.setObjectName(u"en_desig")

        self.verticalLayout.addWidget(self.en_desig)

        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lbl_valor = QLabel(UiDesig)
        self.lbl_valor.setObjectName(u"lbl_valor")

        self.verticalLayout_2.addWidget(self.lbl_valor)

        self.en_valor = QLineEdit(UiDesig)
        self.en_valor.setObjectName(u"en_valor")

        self.verticalLayout_2.addWidget(self.en_valor)

        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lbl_cdc = QLabel(UiDesig)
        self.lbl_cdc.setObjectName(u"lbl_cdc")

        self.verticalLayout_3.addWidget(self.lbl_cdc)

        self.en_cdc = QLineEdit(UiDesig)
        self.en_cdc.setObjectName(u"en_cdc")

        self.verticalLayout_3.addWidget(self.en_cdc)

        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lbl_localidade = QLabel(UiDesig)
        self.lbl_localidade.setObjectName(u"lbl_localidade")

        self.verticalLayout_4.addWidget(self.lbl_localidade)

        self.en_localidade = QLineEdit(UiDesig)
        self.en_localidade.setObjectName(u"en_localidade")

        self.verticalLayout_4.addWidget(self.en_localidade)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.btn_enviar_desig = QPushButton(UiDesig)
        self.btn_enviar_desig.setObjectName(u"btn_enviar_desig")

        self.verticalLayout_5.addWidget(self.btn_enviar_desig)

        self.retranslateUi(UiDesig)

        QMetaObject.connectSlotsByName(UiDesig)
    # setupUi

    def retranslateUi(self, UiDesig):
        UiDesig.setWindowTitle(
            QCoreApplication.translate(
                "UiDesig",
                u"Adicionar designa\u00e7\u00e3o",
                None))
        self.lbl_desig.setText(
            QCoreApplication.translate(
                "UiDesig",
                u"Designa\u00e7\u00e3o",
                None))
        self.lbl_valor.setText(
            QCoreApplication.translate(
                "UiDesig", u"Valor Designacao", None))
        self.lbl_cdc.setText(
            QCoreApplication.translate(
                "UiDesig", u"CDC", None))
        self.lbl_localidade.setText(
            QCoreApplication.translate(
                "UiDesig", u"Localidade", None))
        self.btn_enviar_desig.setText(QCoreApplication.translate(
            "UiDesig", u"Adicionar Designa\u00e7\u00e3o", None))
    # retranslateUi
