import os
from datetime import datetime as dt
from os.path import join

import pandas as pd
from retry import retry

import _main_path
from Automations.Embratel.App_Fatura_Facil.components.convert_fat_to_csv import \
    convert_files  # noqa

_main_path.__loader__


@retry(tries=2, delay=2)
def Read_fats(mesref: dt):
    df = pd.DataFrame()
    mesref = mesref.strftime('%Y-%m')

    automation_path = join(os.environ['OneDrive'],
                           "Clientes\\COMERCIAL\\ICATU\\GESTÃO",
                           "02 - AUTOMACOES")

    ebt_fat_path = join(automation_path,
                        "FAT_EBT",
                        mesref)

    for path in os.listdir(ebt_fat_path):
        full_path = join(ebt_fat_path, path)

        if os.path.isdir(full_path):
            temp_df = convert_files(full_path, categoria=path)
            print('Processado a pasta %s' % path)

            temp_df = temp_df[[
                'NOME_ARQUIVO',
                'FATURA',
                'TIPO_SERVICO',
                'COD_ORIGEM',
                'ORIGEM',
                'CATEGORIA',
                'VALOR'
            ]]

            temp_df = temp_df.loc[temp_df['TIPO_SERVICO'] != "TZN"]
            cats = temp_df['TIPO_SERVICO'].unique().tolist()
            cats_txt = '/'.join(cats)

            temp_df['FILENAME'] = (temp_df['FATURA'].str.removeprefix('FAT_')
                                   + f' ({cats_txt})')

            temp_df['OPERADORA'] = 'Embratel'

            df = pd.concat([df, temp_df])

    df.drop_duplicates(['ORIGEM', 'TIPO_SERVICO', 'COD_ORIGEM'], inplace=True)
    # A COLUNA VALOR ESTÁ VINDO COM OS VALORES ERRADOS
    df.to_csv('db (com erro).csv', sep=';', encoding='utf-8')


if __name__ == "__main__":
    jan = dt(2024, 1, 1)
    Read_fats(jan)
