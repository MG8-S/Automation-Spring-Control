# -*- coding: utf-8 -*-

##########################################################################
# Form generated from reading UI file 'main.ui'
##
# Created by: Qt User Interface Compiler version 6.7.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##########################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
                               QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar, QPushButton,
                               QSizePolicy, QSplitter, QStatusBar,
                               QTableWidget, QTableWidgetItem, QTextEdit,
                               QVBoxLayout, QWidget)


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1104, 682)
        MainWindow.setMinimumSize(QSize(843, 634))
        self.actionImportar_arquivo_CSV = QAction(MainWindow)
        self.actionImportar_arquivo_CSV.setObjectName(
            u"actionImportar_arquivo_CSV")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter_3 = QSplitter(self.centralwidget)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Vertical)
        self.lbl_operadora = QLabel(self.splitter_3)
        self.lbl_operadora.setObjectName(u"lbl_operadora")
        self.splitter_3.addWidget(self.lbl_operadora)
        self.cb_operadora = QComboBox(self.splitter_3)
        self.cb_operadora.setObjectName(u"cb_operadora")
        self.splitter_3.addWidget(self.cb_operadora)

        self.verticalLayout_4.addWidget(self.splitter_3)

        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.lbl_conta = QLabel(self.splitter_2)
        self.lbl_conta.setObjectName(u"lbl_conta")
        self.splitter_2.addWidget(self.lbl_conta)
        self.cb_conta = QComboBox(self.splitter_2)
        self.cb_conta.setObjectName(u"cb_conta")
        self.splitter_2.addWidget(self.cb_conta)

        self.verticalLayout_4.addWidget(self.splitter_2)

        self.splitter_9 = QSplitter(self.centralwidget)
        self.splitter_9.setObjectName(u"splitter_9")
        self.splitter_9.setOrientation(Qt.Vertical)
        self.lbl_tipo = QLabel(self.splitter_9)
        self.lbl_tipo.setObjectName(u"lbl_tipo")
        self.splitter_9.addWidget(self.lbl_tipo)
        self.en_tipo = QComboBox(self.splitter_9)
        self.en_tipo.addItem("")
        self.en_tipo.addItem("")
        self.en_tipo.addItem("")
        self.en_tipo.addItem("")
        self.en_tipo.addItem("")
        self.en_tipo.addItem("")
        self.en_tipo.setObjectName(u"en_tipo")
        self.splitter_9.addWidget(self.en_tipo)

        self.verticalLayout_4.addWidget(self.splitter_9)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lbl_mesref = QLabel(self.centralwidget)
        self.lbl_mesref.setObjectName(u"lbl_mesref")

        self.verticalLayout_2.addWidget(self.lbl_mesref)

        self.en_mesref = QLineEdit(self.centralwidget)
        self.en_mesref.setObjectName(u"en_mesref")
        self.en_mesref.setEnabled(True)

        self.verticalLayout_2.addWidget(self.en_mesref)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lbl_doc = QLabel(self.centralwidget)
        self.lbl_doc.setObjectName(u"lbl_doc")

        self.verticalLayout_3.addWidget(self.lbl_doc)

        self.en_num_documento = QLineEdit(self.centralwidget)
        self.en_num_documento.setObjectName(u"en_num_documento")
        self.en_num_documento.setEnabled(True)

        self.verticalLayout_3.addWidget(self.en_num_documento)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.splitter_8 = QSplitter(self.centralwidget)
        self.splitter_8.setObjectName(u"splitter_8")
        self.splitter_8.setOrientation(Qt.Vertical)
        self.lbl_valor = QLabel(self.splitter_8)
        self.lbl_valor.setObjectName(u"lbl_valor")
        self.splitter_8.addWidget(self.lbl_valor)
        self.en_valor = QLineEdit(self.splitter_8)
        self.en_valor.setObjectName(u"en_valor")
        self.en_valor.setEnabled(True)
        self.splitter_8.addWidget(self.en_valor)

        self.verticalLayout_4.addWidget(self.splitter_8)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.lbl_vencimento = QLabel(self.splitter)
        self.lbl_vencimento.setObjectName(u"lbl_vencimento")
        self.splitter.addWidget(self.lbl_vencimento)
        self.cb_dt_vencimento = QDateEdit(self.splitter)
        self.cb_dt_vencimento.setObjectName(u"cb_dt_vencimento")
        self.cb_dt_vencimento.setWrapping(False)
        self.cb_dt_vencimento.setFrame(True)
        self.cb_dt_vencimento.setMinimumDateTime(
            QDateTime(QDate(2024, 1, 1), QTime(0, 0, 0)))
        self.cb_dt_vencimento.setMaximumDate(QDate(2030, 12, 31))
        self.cb_dt_vencimento.setMinimumDate(QDate(2024, 1, 1))
        self.cb_dt_vencimento.setCalendarPopup(True)
        self.splitter.addWidget(self.cb_dt_vencimento)

        self.verticalLayout_4.addWidget(self.splitter)

        self.splitter_10 = QSplitter(self.centralwidget)
        self.splitter_10.setObjectName(u"splitter_10")
        self.splitter_10.setOrientation(Qt.Vertical)
        self.lbl_emissao = QLabel(self.splitter_10)
        self.lbl_emissao.setObjectName(u"lbl_emissao")
        self.splitter_10.addWidget(self.lbl_emissao)
        self.cb_dt_emissao = QDateEdit(self.splitter_10)
        self.cb_dt_emissao.setObjectName(u"cb_dt_emissao")
        self.cb_dt_emissao.setWrapping(False)
        self.cb_dt_emissao.setFrame(True)
        self.cb_dt_emissao.setMinimumDateTime(
            QDateTime(
                QDate(
                    2024, 1, 1), QTime(
                    0, 0, 0)))
        self.cb_dt_emissao.setMaximumDate(QDate(2030, 12, 31))
        self.cb_dt_emissao.setMinimumDate(QDate(2024, 1, 1))
        self.cb_dt_emissao.setCalendarPopup(True)
        self.splitter_10.addWidget(self.cb_dt_emissao)

        self.verticalLayout_4.addWidget(self.splitter_10)

        self.splitter_4 = QSplitter(self.centralwidget)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Vertical)
        self.lbl_local = QLabel(self.splitter_4)
        self.lbl_local.setObjectName(u"lbl_local")
        self.splitter_4.addWidget(self.lbl_local)
        self.en_local = QLineEdit(self.splitter_4)
        self.en_local.setObjectName(u"en_local")
        self.en_local.setEnabled(True)
        self.splitter_4.addWidget(self.en_local)

        self.verticalLayout_4.addWidget(self.splitter_4)

        self.splitter_5 = QSplitter(self.centralwidget)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Vertical)
        self.lbl_cdc = QLabel(self.splitter_5)
        self.lbl_cdc.setObjectName(u"lbl_cdc")
        self.splitter_5.addWidget(self.lbl_cdc)
        self.en_cdc = QLineEdit(self.splitter_5)
        self.en_cdc.setObjectName(u"en_cdc")
        self.en_cdc.setEnabled(True)
        self.splitter_5.addWidget(self.en_cdc)

        self.verticalLayout_4.addWidget(self.splitter_5)

        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_select_file = QPushButton(self.centralwidget)
        self.btn_select_file.setObjectName(u"btn_select_file")

        self.horizontalLayout_2.addWidget(self.btn_select_file)

        self.lbl_file = QLabel(self.centralwidget)
        self.lbl_file.setObjectName(u"lbl_file")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lbl_file.sizePolicy().hasHeightForWidth())
        self.lbl_file.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.lbl_file)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tbl_designacoes = QTableWidget(self.centralwidget)
        if (self.tbl_designacoes.columnCount() < 4):
            self.tbl_designacoes.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tbl_designacoes.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tbl_designacoes.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tbl_designacoes.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tbl_designacoes.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tbl_designacoes.setObjectName(u"tbl_designacoes")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.tbl_designacoes.sizePolicy().hasHeightForWidth())
        self.tbl_designacoes.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.tbl_designacoes)

        self.frame_direita = QSplitter(self.centralwidget)
        self.frame_direita.setObjectName(u"frame_direita")
        self.frame_direita.setOrientation(Qt.Vertical)
        self.bl_observacoes = QLabel(self.frame_direita)
        self.bl_observacoes.setObjectName(u"bl_observacoes")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.bl_observacoes.sizePolicy().hasHeightForWidth())
        self.bl_observacoes.setSizePolicy(sizePolicy2)
        self.frame_direita.addWidget(self.bl_observacoes)
        self.en_observacoes = QTextEdit(self.frame_direita)
        self.en_observacoes.setObjectName(u"en_observacoes")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.en_observacoes.sizePolicy().hasHeightForWidth())
        self.en_observacoes.setSizePolicy(sizePolicy3)
        self.frame_direita.addWidget(self.en_observacoes)

        self.verticalLayout.addWidget(self.frame_direita)

        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_add_designacao = QPushButton(self.centralwidget)
        self.btn_add_designacao.setObjectName(u"btn_add_designacao")

        self.horizontalLayout.addWidget(self.btn_add_designacao)

        self.btn_validar_rateio = QPushButton(self.centralwidget)
        self.btn_validar_rateio.setObjectName(u"btn_validar_rateio")

        self.horizontalLayout.addWidget(self.btn_validar_rateio)

        self.btn_enviar_rateio = QPushButton(self.centralwidget)
        self.btn_enviar_rateio.setObjectName(u"btn_enviar_rateio")

        self.horizontalLayout.addWidget(self.btn_enviar_rateio)

        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1104, 26))
        self.menuFun_es = QMenu(self.menubar)
        self.menuFun_es.setObjectName(u"menuFun_es")
        self.menuEmbratel = QMenu(self.menuFun_es)
        self.menuEmbratel.setObjectName(u"menuEmbratel")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.cb_operadora, self.cb_conta)
        QWidget.setTabOrder(self.cb_conta, self.en_tipo)
        QWidget.setTabOrder(self.en_tipo, self.en_mesref)
        QWidget.setTabOrder(self.en_mesref, self.en_num_documento)
        QWidget.setTabOrder(self.en_num_documento, self.en_valor)
        QWidget.setTabOrder(self.en_valor, self.cb_dt_vencimento)
        QWidget.setTabOrder(self.cb_dt_vencimento, self.cb_dt_emissao)
        QWidget.setTabOrder(self.cb_dt_emissao, self.en_local)
        QWidget.setTabOrder(self.en_local, self.en_cdc)
        QWidget.setTabOrder(self.en_cdc, self.btn_select_file)
        QWidget.setTabOrder(self.btn_select_file, self.tbl_designacoes)
        QWidget.setTabOrder(self.tbl_designacoes, self.en_observacoes)
        QWidget.setTabOrder(self.en_observacoes, self.btn_add_designacao)
        QWidget.setTabOrder(self.btn_add_designacao, self.btn_validar_rateio)
        QWidget.setTabOrder(self.btn_validar_rateio, self.btn_enviar_rateio)

        self.menubar.addAction(self.menuFun_es.menuAction())
        self.menuFun_es.addAction(self.menuEmbratel.menuAction())
        self.menuEmbratel.addAction(self.actionImportar_arquivo_CSV)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow", u"Rateios - Icatu", None))
        self.actionImportar_arquivo_CSV.setText(
            QCoreApplication.translate(
                "MainWindow", u"Importar arquivo CSV", None))
        self.lbl_operadora.setText(
            QCoreApplication.translate(
                "MainWindow", u"Operadora", None))
        self.lbl_conta.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"N\u00famero da Conta",
                None))
        self.lbl_tipo.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"Tipo de conta",
                None))
        self.en_tipo.setItemText(
            0, QCoreApplication.translate(
                "MainWindow", u"Tel. Fixa", None))
        self.en_tipo.setItemText(
            1, QCoreApplication.translate(
                "MainWindow", u"Tel. 0800", None))
        self.en_tipo.setItemText(
            2, QCoreApplication.translate(
                "MainWindow", u"Tel. SNU", None))
        self.en_tipo.setItemText(
            3, QCoreApplication.translate(
                "MainWindow", u"Dados", None))
        self.en_tipo.setItemText(
            4, QCoreApplication.translate(
                "MainWindow", u"Cloud", None))
        self.en_tipo.setItemText(
            5, QCoreApplication.translate(
                "MainWindow", u"Arbor", None))

        self.lbl_mesref.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"M\u00eas de refer\u00eancia",
                None))
        self.lbl_doc.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"N\u00famero do documento",
                None))
        self.lbl_valor.setText(
            QCoreApplication.translate(
                "MainWindow", u"Valor rateio", None))
        self.lbl_vencimento.setText(
            QCoreApplication.translate(
                "MainWindow", u"Vencimento", None))
        self.lbl_emissao.setText(
            QCoreApplication.translate(
                "MainWindow", u"Emiss\u00e3o", None))
        self.lbl_local.setText(
            QCoreApplication.translate(
                "MainWindow", u"Localidade", None))
        self.lbl_cdc.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"Centro de Custo",
                None))
        self.btn_select_file.setText(
            QCoreApplication.translate(
                "MainWindow", u"Selecionar Arquivo", None))
        self.lbl_file.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"Selecione o arquivo a ser anexo...",
                None))
        ___qtablewidgetitem = self.tbl_designacoes.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"Designa\u00e7\u00e3o",
                None))
        ___qtablewidgetitem1 = self.tbl_designacoes.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate(
                "MainWindow", u"Valor", None))
        ___qtablewidgetitem2 = self.tbl_designacoes.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate(
                "MainWindow", u"Centro de Custo", None))
        ___qtablewidgetitem3 = self.tbl_designacoes.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate(
                "MainWindow", u"Localidade", None))
        self.bl_observacoes.setText(
            QCoreApplication.translate(
                "MainWindow",
                u"Observa\u00e7\u00f5es",
                None))
        self.btn_add_designacao.setText(QCoreApplication.translate(
            "MainWindow", u"Adicionar Designa\u00e7\u00e3o", None))
        self.btn_validar_rateio.setText(
            QCoreApplication.translate(
                "MainWindow", u"Validar rateio", None))
        self.btn_enviar_rateio.setText(
            QCoreApplication.translate(
                "MainWindow", u"Enviar rateio", None))
        self.menuFun_es.setTitle(
            QCoreApplication.translate(
                "MainWindow", u"Importar", None))
        self.menuEmbratel.setTitle(
            QCoreApplication.translate(
                "MainWindow", u"Embratel", None))
    # retranslateUi
