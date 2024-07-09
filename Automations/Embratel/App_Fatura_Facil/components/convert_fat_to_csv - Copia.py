import os
import pandas as pd

try:
    path = os.path.dirname(__file__)
except Exception:
    path = os.getcwd()


def convert_files(path: str,
                  output_path: str = None,
                  output_name_log: str = "FATURA_PROCESSADA",
                  categoria: str = None):

    if not output_path:
        output_path = path

    arquivo = os.listdir(path)
    cont = 0
    for nome_arquivo in arquivo:
        if 'py' in nome_arquivo or output_name_log in nome_arquivo:
            continue

        path_file = os.path.join(path, nome_arquivo)
        filename = nome_arquivo.split()[-1]
        filename = filename.removesuffix('.TXT')

        if cont == 0:
            df = pd.read_csv(path_file, encoding="latin",
                             dtype='str', names=['LINHA'], engine='pyarrow')
            df.insert(0, 'ID', df.index + 1)
            df.insert(2, 'NOME_ARQUIVO', nome_arquivo)

            df.insert(2, 'FATURA', filename)
            # df.insert(2, 'NUM_CONTA', STRING)
            cont = cont + 1
        else:
            dfx = pd.read_csv(path_file, encoding="latin",
                              dtype='str', names=['LINHA'], engine='pyarrow')
            dfx.insert(0, 'ID', dfx.index + 1)
            dfx.insert(2, 'NOME_ARQUIVO', nome_arquivo)

            dfx.insert(2, 'FATURA', filename)
            # df.insert(2, 'NUM_CONTA', STRING)
            df = pd.concat([df, dfx], ignore_index=True)
            cont = cont + 1

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

    df_chamada.insert(1, 'COD_SEQ_ITEM',
                      df_chamada['LINHA'].str[7:14].str.strip())

    df_outros.insert(1, 'COD_SEQ_ITEM',
                     df_outros['LINHA'].str[7:14].str.strip())

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

    df_chamada.insert(3, 'HORA', (df_chamada['LINHA'].str[191:193]
                                  .str.strip() + ":" +
                                  df_chamada['LINHA'].str[193:195]
                                  .str.strip() + ":" +
                                  df_chamada['LINHA'].str[195:197]
                                  .str.strip()))

    df_outros.insert(3, 'HORA', '')

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

    df_chamada.insert(1, 'UNIDADE', (df_chamada['LINHA'].str[157:163]
                                     .str.strip()))

    df_outros.insert(1, 'UNIDADE', (df_outros['LINHA'].str[157:163]
                                    .str.strip()))

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

    df_chamada.insert(1, 'COD_DESTINO', (df_chamada['LINHA'].str[184:191]
                                         .str.strip()))

    df_outros.insert(1, 'COD_DESTINO', '')

    df_result = pd.concat([df_chamada, df_outros], ignore_index=True)

    # AJUSTANDO ORDEM COLUNAS
    columns = [
        'ID',
        'COD_SEQ_ITEM',
        'NOME_ARQUIVO',
        'FATURA',
        'TIPO_SERVICO',
        'DATA_INICIO',
        'DATA_FIM',
        'HORA',
        'ORIGEM',
        'DESTINO',
        'COD_ORIGEM',
        'COD_DESTINO',
        'LOCAL_ORIGEM',
        'SERVICO_COMPLETO',
        'QUANTIDADE/MINUTOS',
        'UNIDADE',
        'VALOR',
    ]

    if categoria:
        columns.append("CATEGORIA")

    columns.append("LINHA")
    df_result = df_result[columns]

    df_result.to_csv(os.path.join(output_path, output_name_log + '.csv'),
                     index=False, sep=';', encoding='utf-8',
                     float_format='%.4f', decimal=",")

    return df_result
