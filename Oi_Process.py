import os
import pandas as pd

from datetime import datetime as dt
from datetime import timedelta as td

from Automations.Oi.down_det_oi import down_det_oi
from Readers.Oi.Leitor_Boleto_OI import ler_boleto_oi
from Readers.Oi.Leitor_Detalhamentos_OI import leitor_detalhamento_oi
from Readers.Oi.Leitor_Rateio_OI import get_rateio


def Oi_Process(mes: dt):
    mesref = mes.strftime('%Y-%m')
    oi_path = os.path.join(os.environ['OneDrive'],
                           "Clientes/COMERCIAL/ICATU/GESTÃO/02 - AUTOMACOES/",
                           f"PARA TRATAR/{mesref}/OI")

    details_path = os.path.join(oi_path, "DETALHAMENTOS")

    df_invoices = fr"{os.environ['OneDrive']}\Publico\NYCOLAS\01 - PROJETOS\Automacao Spring Control\Logs\oi_files.csv"
    init_date = (dt(mes.year, mes.month, 1))
    final_date = (dt(mes.year, mes.month + 1, 1) - td(1))

    os.chdir(os.path.dirname(__file__))

    # print('\n|', '='*100, '|')
    print("Lendo boletos baixados da Oi...")
    ler_boleto_oi(oi_path)

    # Abaixa o datalhamento das faturas OI
    print('\n|', '=' * 100, '|')
    print("Baixando detalhamentos da Oi...")
    down_det_oi(details_path, init_date, final_date)

    # Lê o arquivo gerado e gera um arquivo com os detalhamentos
    print('\n|', '=' * 100, '|')
    print("Gerando detalhamento da Oi...")
    df_invoices = pd.read_csv(df_invoices, sep=';',
                              encoding='utf-8', dtype=str)
    df_oi_det = leitor_detalhamento_oi(details_path, df_invoices, mesref)

    # Gerando o rateio da OI
    print('\n|', '=' * 100, '|')
    print("Gerando o rateio da Oi...")
    get_rateio(mesref, df_oi_det, export=True)

    print('\n|', '=' * 100, '|')
    print("Processo finalizado com sucesso!")


# Main function execution starts here
if __name__ == "__main__":
    # today = (dt(2024, 7, 1))
    today = (dt.now())
    Oi_Process(today)
