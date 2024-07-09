import os
from datetime import datetime as dt
from Automations.Embratel.App_Fatura_Facil.Fat_Converter import Read_fats  # noqa
from Automations.Embratel.App_Fatura_Facil.main import Download_Fat_Ebt
from Readers.Embratel.Leitor_Fat import Process_Fat_Ebt


def Ebt_Process(mes: dt):
    # Process detailed billing report for Embratel
    try:
        app_path = os.path.join(
            os.path.dirname(__file__),
            'Automations/Embratel/App_Fatura_Facil/app'
        )
        for file in os.listdir(app_path):
            if file.endswith('.TXT'):
                os.remove(os.path.join(app_path, file))

        Download_Fat_Ebt(mes)
        Read_fats(mes)
        # Process_Fat_Ebt()
    except Exception as e:
        print(e)


# Main function
if __name__ == '__main__':
    Ebt_Process(dt.now())
