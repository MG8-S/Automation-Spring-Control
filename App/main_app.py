import os
import sys
from datetime import datetime as dt

try:
    import pandas as pd
    from PySide6.QtGui import QPixmap
    from PySide6.QtWidgets import (QApplication, QFileDialog, QMessageBox,
                                   QTableWidgetItem)
    from Screens.add_desig import Ui_Desig
    from Screens.main_screen import Ui_MainWindow
except ModuleNotFoundError as mnfe:
    os.system(f"pip install {mnfe.name}")
    os.system(f"python \"{__file__}\"")
    quit()


class Notification_App(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(
            QPixmap(os.path.abspath('app/src/notification.png')))

    def send_notification(self, title, message):
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()


class App_Designacoes(Ui_Desig):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.app_desig = None  # Adicione este atributo

    def get_info(self) -> None | dict:
        info = {}
        info['cdc'] = self.en_cdc.text()
        info['localidade'] = self.en_localidade.text()
        info['designacao'] = self.en_desig.text()
        info['valor'] = self.en_valor.text()

        for key, value in info.items():
            if value == '':
                print(f'Por favor, preencha o valor do campo "{key}"')
                return

        self.close()

        return info


class App(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QPixmap(os.path.abspath('app/src/settings.png')))
        self.notification_app = Notification_App()

        self.history_path = f'{os.environ["OneDrive"]}\\Clientes\\COMERCIAL\\ICATU\\GESTÃO\\01 - ARQUIVOS MENSAIS\\HISTÓRICO V1.xlsx'
        self.df = self.__read_history__('FATURAS (DOING)')
        self.df_desig = self.__read_history__('DESIGNAÇÕES (OPERADORA)')

        self.file = None
        self.config_screen()

        self.cb_operadora.currentIndexChanged.connect(self.change_contas)
        self.btn_select_file.clicked.connect(self.select_file)
        self.btn_validar_rateio.clicked.connect(self.view_info)
        self.btn_add_designacao.clicked.connect(self.add_designacao)
        # self.btn_enviar_rateio.clicked.connect(self.send_rateio)
        self.btn_enviar_rateio.clicked.connect(
            lambda: self.__add_in_table__('Teste'))

    def config_screen(self) -> None:
        operadoras = self.df['OPERADORA'].unique().tolist()
        print(operadoras)
        self.cb_operadora.addItems(operadoras)
        self.change_contas()
        self.en_mesref.setText(dt.now().strftime('%Y-%m'))

    def add_designacao(self) -> None:
        self.app_desig = App_Designacoes()  # Armazena a instância
        self.app_desig.en_desig.textChanged.connect(self.change_designacao)
        self.app_desig.show()
        self.app_desig.btn_enviar_desig.clicked.connect(self.get_desig_info)

    def change_designacao(self) -> None:
        operadora = self.cb_operadora.currentText()
        conta = self.cb_conta.currentText()
        desig = self.app_desig.en_desig.text()

        if desig == '':
            self.app_desig.en_cdc.setText('')
            self.app_desig.en_localidade.setText('')
            return

        df_temp = self.df_desig.loc[
            (self.df_desig['OPERADORA'] == operadora)
            & (self.df_desig['FATURA'] == conta)
            & (self.df_desig['DESIGNAÇÃO'].str.contains(str(desig)))]

        if not df_temp.empty:
            cdc = df_temp['CDC'].to_list()[0]
            localidade = df_temp['LOCALIDADE'].to_list()[0]

            self.app_desig.en_cdc.setText(cdc)
            self.app_desig.en_localidade.setText(localidade)

    def get_desig_info(self) -> None:
        info = self.app_desig.get_info()
        info_item = QTableWidgetItem(text="Test")
        self.tbl_designacoes.setItem(1, 1, info_item)

    def change_contas(self) -> None:
        self.cb_conta.clear()
        current_op = self.cb_operadora.currentText()
        current_contas = self.df.loc[self.df['OPERADORA'] == current_op,
                                     'COD_FATURA'].unique().tolist()
        self.cb_conta.addItems(current_contas)

    def select_file(self) -> None:
        self.file, _ = QFileDialog.getOpenFileName(self,
                                                   "Selecionar Arquivo",
                                                   "",
                                                   "Arquivos PDF (*.pdf)")

        self.lbl_file.setText(os.path.basename(self.file))

    def view_info(self) -> None:
        operadora = self.cb_operadora.currentText()
        conta = self.cb_conta.currentText()
        tipo = self.en_tipo.currentText()
        mesref = self.en_mesref.text()
        num_doc = self.en_num_documento.text()
        total_value = self.en_valor.text()
        vencimento = self.cb_dt_vencimento.text()
        emissao = self.cb_dt_emissao.text()
        localidade = self.en_local.text()
        cdc = self.en_cdc.text()
        observacoes = self.en_observacoes.toPlainText()
        arquivo = self.file

        print(operadora, conta, tipo, localidade, arquivo, cdc,
              mesref, num_doc, total_value, vencimento, emissao)
        print(observacoes)

    def __add_in_table__(self, text, icon=None, align=None):
        print(text)
        item = QTableWidgetItem(text=text)

        if icon is not None:
            item.setIcon(icon)

        if align is not None:
            pass
        self.tbl_designacoes.setItem(self.tbl_designacoes.rowCount(), 1, item)

    def __read_history__(self, sheet_name: str) -> pd.DataFrame:
        df = pd.read_excel(self.history_path, sheet_name=sheet_name)
        print(df)

        return df


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
