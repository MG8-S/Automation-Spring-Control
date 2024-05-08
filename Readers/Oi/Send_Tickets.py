import locale
import os
import re

import pandas as pd
from pandas import Series

import _main_path
from Objects.Obj_Databases import ControlDatabases
from Objects.Obj_EmailSender import Email

_main_path.__loader__
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def __send_error_email(info: Series) -> None:
    pass


def __send_ticket_email__(info: Series) -> None:
    email = Email()

    operadora = info["operadora"]
    localidade = info["localidade"]
    conta = info["conta"]
    vencimento = info["vencimento"]

    subject = f"Fatura {operadora} - {localidade} - Vencimento {vencimento} - Número da conta {conta}"  # noqa
    # email.destination = []
    # email.cc = []
    # email.bcc = []
    # email.subject = subject
    print(subject)


def __save_on_db__(info: Series) -> None:
    db = ControlDatabases("faturas_enviadas.db")
    # columns = db.__get_table_info__("status_faturas")
    # print(columns)
    db


def __concat_with_history__(df: pd.DataFrame, file: str, sheet_name: str) -> pd.DataFrame:  # noqa
    history_df = pd.read_excel(file, sheet_name=sheet_name)

    # Extrair os valores de 'conta' de df como uma lista
    conta_list = df['conta'].tolist()

    # Adicionar uma nova coluna 'CONTA' a history_df contendo valores em
    # comum com 'conta_list'
    history_df['CONTA'] = history_df['COD_FATURA'].apply(
        lambda x: next((conta for conta in conta_list if conta in x), None))

    # Mesclar os DataFrames com base na coluna 'OPERADORA' e 'CONTA'
    merged_df = df.merge(history_df,
                         how='left',
                         left_on=['operadora', 'conta'],
                         right_on=['OPERADORA', 'CONTA'])

    return merged_df


def process_ticket(df: pd.DataFrame) -> None:
    history_pathfile = fr"{os.environ['OneDrive']}\Clientes\COMERCIAL\ICATU\GESTÃO\01 - ARQUIVOS MENSAIS\HISTÓRICO V1.xlsx"
    sheet_name = "FATURAS (DOING)"
    main_df = __concat_with_history__(df, history_pathfile, sheet_name)

    process_ticket(main_df)
    for i, row in df.iterrows():
        try:
            # __send_ticket_email__(row)
            pass
        except Exception as e:
            print("Erro em enviar e-mail:", e)
        else:
            print(f'Boleto {row["conta"]} salvo com sucesso')
            # __save_on_db__(row)


if __name__ == '__main__':
    db = ControlDatabases("faturas_enviadas.db")

    df = pd.read_csv(
        fr"{os.environ['OneDrive']}\Publico\NYCOLAS\01 - PROJETOS\Automacao Spring Control\Logs\oi_files.csv",
        sep=';',
        decimal=',',
        encoding='utf-8')

    history_pathfile = fr"{os.environ['OneDrive']}\Clientes\COMERCIAL\ICATU\GESTÃO\01 - ARQUIVOS MENSAIS\HISTÓRICO V1.xlsx"
    sheet_name = "FATURAS (DOING)"
    main_df = __concat_with_history__(df, history_pathfile, sheet_name)

    print(main_df)

    main_df.to_excel('t.xlsx', index=False)

    # process_ticket(main_df)
