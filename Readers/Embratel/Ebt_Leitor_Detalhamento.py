import os
import _main_path
import traceback
import pandas as pd
import numpy as np

from os.path import join

from Readers.Embratel.convert_file_to_df import convert_file

_main_path.__loader__


def find_file_det(string: str, files_list: list) -> str | None:
    print(string, end=' -> ')
    string = string.replace('/', '').split('-')[0]
    for f in files_list:
        if string in f:
            print(f)
            return f

    return None


# def get_files(details_path: str) -> list:
details_path = join(
    os.environ['OneDrive'],
    "Clientes/COMERCIAL/ICATU/GESTÃO/02 - AUTOMACOES/FAT_EBT"
)

files_list = []

for path, _, files in os.walk(details_path):
    files_list += [join(path, file) for file in files
                   if file.lower().endswith('.txt')]


# def read_files(files_list: list) -> pd.DataFrame:
df = pd.read_csv('logs/ebt_files.csv', sep=';', encoding='utf-8')

df = df.loc[~df['arquivo'].str.contains('Arbor')]

print(df)

df['path_det'] = df['fatura'].apply(lambda x: find_file_det(x, files_list))

det = convert_file(df.iloc[0].tolist()[-1])
