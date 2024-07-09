import os
import pandas as pd

try:
    path = os.path.dirname(__file__)
except Exception:
    path = os.getcwd()


def convert_file(path_file: str,
                 categoria: str = None):

    if not os.path.isfile(path_file):
        raise Exception(
            f'Arquivo {path_file} não encontrado ou não é um arquivo.')

    nome_arquivo = os.path.basename(path_file)
    filename = nome_arquivo.split()[-1]
    filename = filename.removesuffix('.TXT')

    df = pd.read_csv(path_file, encoding="latin",
                     dtype='str', names=['LINHA'], engine='pyarrow')
    df.insert(0, 'ID', df.index + 1)
    df.insert(2, 'NOME_ARQUIVO', nome_arquivo)

    df.insert(2, 'FATURA', filename)
    # df.insert(2, 'NUM_CONTA', STRING)

    df['LINHA'] = (df['LINHA'].str.replace('\\', '')
                   .str.replace('x00', '|')
                   .str.replace("b'", '')
                   .str.replace("'", '')
                   .str.replace('xe7', 'C')
                   .str.replace('xe3', 'A'))

    df['SERVICO_COMPLETO'] = df['LINHA'].str[95:145].str.strip()

    if categoria:
        df['CATEGORIA'] = categoria

    df_chamada = df[df['LINHA'].str[95:103].str.strip() == 'CHAMADA']
    df_outros = df[df['LINHA'].str[95:103].str.strip() != 'CHAMADA']

    df_chamada.insert(1, 'TIPO_SERVICO',
                      df_chamada['LINHA'].str[2:7].str.strip())

    df_outros.insert(1, 'TIPO_SERVICO',
                     df_outros['LINHA'].str[2:7].str.strip())

    df_chamada.insert(2, 'DATA_INICIO', (df_chamada['LINHA'].str[18:20]
                                         .str.strip()
                                         + "/" + df_chamada['LINHA'].str[16:18]
                                         .str.strip() + "/" + "20" +
                                         df_chamada['LINHA'].str[14:16]
                                         .str.strip()))

    df_outros.insert(2, 'DATA_INICIO', (df_outros['LINHA'].str[18:20]
                                        .str.strip() + "/" +
                                        df_outros['LINHA'].str[16:18]
                                        .str.strip() + "/" + "20" +
                                        df_outros['LINHA'].str[14:16]
                                        .str.strip()))

    df_chamada.insert(3, 'DATA_FIM', (df_chamada['LINHA'].str[24:26]
                                      .str.strip() + "/" +
                                      df_chamada['LINHA'].str[22:24]
                                      .str.strip() + "/" + "20" +
                                      df_chamada['LINHA'].str[20:22]
                                      .str.strip()))

    df_outros.insert(3, 'DATA_FIM', (df_outros['LINHA'].str[24:26]
                                     .str.strip() + "/" +
                                     df_outros['LINHA'].str[22:24]
                                     .str.strip() + "/" + "20" +
                                     df_outros['LINHA'].str[20:22]
                                     .str.strip()))

    df_chamada.insert(3, 'ORIGEM', (df_chamada['LINHA'].str[26:38]
                                    .str.strip()
                                    .str.replace(' ', '')
                                    .str.replace('-', '')))

    df_outros.insert(3, 'ORIGEM', (df_outros['LINHA'].str[26:38]
                                   .str.strip()
                                   .str.replace(' ', '')
                                   .str.replace('-', '')))

    df_chamada.insert(3, 'LOCAL_ORIGEM', (df_chamada['LINHA'].str[50:75]
                                          .str.replace('|', '')
                                          .str.strip()
                                          .str.replace('-', '')))

    df_outros.insert(3, 'LOCAL_ORIGEM', (df_outros['LINHA'].str[38:95]
                                         .str.replace('|', '')
                                         .str.strip()
                                         .str.replace('-', '')))

    df_chamada.insert(3, 'DESTINO', (df_chamada['LINHA'].str[75:95]
                                     .str.strip()
                                     .str.replace('-', '')))

    df_outros.insert(3, 'DESTINO', '')

    df_chamada.insert(2, 'QUANTIDADE/MINUTOS',
                      pd.to_numeric(df_chamada['LINHA'].str[145:157]) / 1000)

    df_outros.insert(2, 'QUANTIDADE/MINUTOS',
                     pd.to_numeric(df_outros['LINHA'].str[145:157]) / 1000)

    df_chamada.insert(2, 'VALOR',
                      (pd.to_numeric(df_chamada['LINHA'].str[1:2] +
                                     df_chamada['LINHA'].str[163:174]) / 100))

    df_outros.insert(2, 'VALOR',
                     (pd.to_numeric(df_outros['LINHA'].str[1:2] +
                                    df_outros['LINHA'].str[163:174]) / 100))

    df_chamada.insert(1, 'COD_ORIGEM', (df_chamada['LINHA'].str[177:184]
                                        .str.strip()))

    df_outros.insert(1, 'COD_ORIGEM', (df_outros['LINHA'].str[177:184]
                                       .str.strip()))

    df_result = pd.concat([df_chamada, df_outros], ignore_index=True)

    # AJUSTANDO ORDEM COLUNAS
    columns = [
        'ID',
        'NOME_ARQUIVO',
        'FATURA',
        'TIPO_SERVICO',
        'DATA_INICIO',
        'DATA_FIM',
        'ORIGEM',
        'COD_ORIGEM',
        'LOCAL_ORIGEM',
        'SERVICO_COMPLETO',
        'VALOR',
    ]

    if categoria:
        columns.append("CATEGORIA")

    columns.append("LINHA")
    df_result = df_result[columns]

    # df_result.to_csv(os.path.join(output_path, output_name_log + '.csv'),
    #                  index=False, sep=';', encoding='utf-8',
    #                  float_format='%.4f', decimal=",")

    return df_result
