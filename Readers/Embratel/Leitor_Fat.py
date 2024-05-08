import os
import locale
import _main_path
import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup

from os.path import join
from datetime import datetime as dt

from Objects.Obj_EmailSender import Email
from Objects.Obj_Databases import ControlDatabases

_main_path.__loader__
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
hoje = dt.now().strftime('%d/%m/%Y')
mesref = dt.now().strftime('%Y-%m')


def get_sended_invoices():
    db = ControlDatabases("ebt_database.db")
    db.create_table(table_name='faturas_analisadas',
                    columns={'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                             'fatura': 'TEXT',
                             'data_envio': 'DATETIME',
                             'mesref': 'TEXT'
                             })

    faturas_enviadas = db.command(f"""
               select
                    fatura
               from
                    faturas_analisadas
               where
                    mesref = '{mesref}'""", return_df=False)

    return [x[0] for x in faturas_enviadas]


def send_invoice_email(temp_df, filename):
    # TODO: Linkar e fazer um merge com uma tabela com cdc e localidade
    df = pd.DataFrame()
    df['DESIGNAÇÃO'] = temp_df['ORIGEM']
    df['TIPO'] = None
    df['FORNECEDOR'] = temp_df['OPERADORA']
    df['REF'] = None
    df['NÚM. DOCUMENTO'] = None
    df['EMISSÃO'] = None
    df['DESCRIÇÃO'] = temp_df['SERVICO_COMPLETO']
    df['CATEGORIA'] = temp_df['TIPO_SERVICO']
    df['VALOR TOTAL'] = temp_df['VALOR_TOTAL']
    df['VALOR RATEIO'] = temp_df['VALOR']
    df['VENCIMENTO'] = None
    df['MÊS VENCIMENTO'] = None
    df['CDC'] = None
    df['LOCALIDADE'] = temp_df['COD_ORIGEM']
    df['ENTREGUE'] = hoje
    df['NÚM. DA CONTA'] = temp_df['FILENAME']

    df = df[
        [
            'FORNECEDOR',
            'REF',
            'NÚM. DOCUMENTO',
            'EMISSÃO',
            'TIPO',
            'DESIGNAÇÃO',
            'DESCRIÇÃO',
            'CATEGORIA',
            'VALOR TOTAL',
            'VALOR RATEIO',
            'VENCIMENTO',
            'MÊS VENCIMENTO',
            'CDC',
            'LOCALIDADE',
            'ENTREGUE',
            'NÚM. DA CONTA'
        ]
    ]

    # Criando e-mail
    fornecedor = df['FORNECEDOR'].iloc[0]
    vencimento = df['VENCIMENTO'].iloc[0]
    num_fatura = df['NÚM. DOCUMENTO'].iloc[0]
    titulo = f"Fatura {fornecedor} - Vencimento: {vencimento} - Número da Conta {num_fatura}"  # noqa
    email = Email(titulo)

    email.destination = ['npimentel@mg8.com.br']
    email.cc = ['nycolaspimentel12@gmail.com']
    email.bcc = ['nycolaspimentel@gmail.com']

    print(email.destination + email.cc + email.bcc)

    df_html = df.to_html(index=False, justify='center', decimal=',',
                         table_id="id-table", col_space=100,
                         show_dimensions=True)

    soup = BeautifulSoup(df_html, 'html.parser')
    for i, row in enumerate(soup.find('tbody').find_all('tr')):
        if i % 2 == 0:
            row['class'] = 'odd'

    email.body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    #body {{
        width: max-content;
        min-width: 600px !important;
        margin: 0 auto; /* Centralizando o conteúdo na tela */
        padding: 0 10px; /* Adicionando um pouco de espaço nas laterais */
    }}

    #id-table {{
        width: 100%; /* Ajustando a largura da tabela para ocupar 100% da largura da div pai */
        text-align: center;
        border-collapse: collapse;
    }}

    #id-table *{{
        white-space: nowrap;
    }}

    #id-table th, #id-table td {{
        border: 1px solid black;
        padding: 5px;
    }}

    thead tr {{
        background-color: rgb(255, 208, 121);
    }}

    thead tr th {{
        padding: 10px;
    }}

    tbody tr.odd {{
        background-color: rgb(219, 219, 219);
    }}
</style>
</head>
<body>
<div id="body">
<p>Prezados, olá.</p>
<p>Segue o rateio:</p>
{soup.prettify()}

<p>Atenciosamente,</p>
<p>Spring Group.</p>
</div>
</body>
</html>
"""

    with open('t.html', 'w', encoding='utf-8') as f:
        f.write(email.body)

    print('\033[1;33mEnviando a fatura %s\033[0m' % filename)
    email.create_email()
    email.send_email(confirm_send_message=False)


def Process_Fat_Ebt():
    invoices_path = join(
        os.environ['OneDrive'],
        r"Clientes\COMERCIAL\ICATU\GESTÃO\02 - AUTOMACOES\FAT_EBT",
        mesref)

    invoices_inventory = join(
        os.environ['OneDrive'],
        r"Clientes\COMERCIAL\ICATU\GESTÃO\01 - ARQUIVOS MENSAIS\HISTÓRICO V1.xlsx"
    )

    inventory_df = pd.read_excel(invoices_inventory, 'DESIGNAÇÕES (OPERADORA)')
    inventory_df = inventory_df.loc[inventory_df['OPERADORA'].str.lower(
    ) == 'embratel']
    inventory_df.drop(columns=['FATURA'], inplace=True)

    inventory_df.to_excel('y.xlsx')
    paths = os.listdir(invoices_path)

    for path in paths[:1]:
        print(path)

        sended_invoices = get_sended_invoices()

        path = join(invoices_path, path)
        files = os.listdir(path)
        file = [f for f in files if '.csv' in f][0]
        path_file = join(path, file)

        main_df = pd.read_csv(path_file, sep=';',
                              encoding='utf-8', decimal=',')
        main_df = main_df[
            [
                'COD_ORIGEM',
                'FATURA',
                'ORIGEM',
                'SERVICO_COMPLETO',
                'TIPO_SERVICO',
                'VALOR',
            ]
        ]

        main_df = main_df.groupby([
            'COD_ORIGEM',
            'FATURA',
            'ORIGEM',
            'SERVICO_COMPLETO',
            'TIPO_SERVICO'
        ]).sum()

        main_df.reset_index(inplace=True)

        main_df['VALOR_TOTAL'] = main_df['VALOR'].sum()

        main_df['VALOR'] = main_df['VALOR'].apply(
            lambda x: locale.currency(x, grouping=True, symbol='R$')
        )

        main_df['VALOR_TOTAL'] = main_df['VALOR_TOTAL'].apply(
            lambda x: locale.currency(x, grouping=True, symbol='R$')
        )

        main_df = main_df.merge(inventory_df,
                                left_on='ORIGEM',
                                right_on='DESIGNAÇÃO',
                                how='left')

        main_df.sort_values(['FATURA', 'ORIGEM', 'TIPO_SERVICO'], inplace=True)
        main_df = main_df.loc[main_df['TIPO_SERVICO'] != "TZN"]
        cats = main_df['TIPO_SERVICO'].unique().tolist()
        cats_txt = '/'.join(cats)

        main_df['FILENAME'] = (main_df['FATURA'].str.removeprefix('FAT_')
                               + f' ({cats_txt})')

        main_df.drop_duplicates(['ORIGEM',
                                'TIPO_SERVICO',
                                 'COD_ORIGEM',
                                 'FILENAME'], inplace=True)

        main_df['OPERADORA'] = 'Embratel'

        for arquivo in main_df['FILENAME'].unique().tolist()[:1]:
            # if arquivo in sended_invoices:
            #     continue

            temp_df = main_df.loc[main_df['FILENAME'] == arquivo]

            temp_df.to_excel('t.xlsx')
            print("")
            send_invoice_email(temp_df, arquivo)

            # db.insert_data('faturas_analisadas',
            #                columns=['fatura', 'data_envio', 'mesref'],
            #                data=[(arquivo, dt.now(), mesref)])


if __name__ == "__main__":
    Process_Fat_Ebt()
