import os
import locale
import jinja2
import openpyxl
import _main_path
import pandas as pd
import numpy as np
from datetime import datetime as dt
from Objects.Obj_Databases import ControlDatabases

jinja2.__loader__
openpyxl.__loader__
_main_path.__loader__
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def create_history_table(db: ControlDatabases) -> None:
    db.create_table(table_name='history_oi', columns={
        'conta': 'TEXT',
        'fatura': 'TEXT',
        'emissao': 'DATE',
        'vencimento': 'DATE',
        'mesref': 'TEXT',
        'ddd': 'TEXT',
        'tipo_leitura': 'INTEGER',
        'origem': 'TEXT',
        'localidade': 'TEXT',
        'cdc': 'TEXT',
        'descricao': 'TEXT',
        'valor_fatura': 'FLOAT',
        'valor_det': 'FLOAT',
        'file_pdf': 'TEXT',
        'file_det': 'TEXT',
    })


def __get_desig(db_faturas: ControlDatabases) -> pd.DataFrame:
    return db_faturas.command("""
        select
            fats.operadora as operadora,
            fats.fatura as fat_fatura,
            fats.cdc as fat_cdc,
            fats.filial as fat_filial,
            fats.observações as fat_observacoes,
            con_dsg.designacao as designacao,
            con_dsg.cdc as desig_cdc,
            con_dsg.tipo as desig_tipo,
            con_dsg.filial as desig_filial,
            con_dsg.observacoes as desig_observacoes
        from
            controle_designacoes as con_dsg
        join
            faturas as fats on fats.id_fatura = con_dsg.id_fatura
        where
            fats.operadora = 'Oi'
    """)


def __get_aux_df_oi(mesref: str,
                    df_oi: None | pd.DataFrame = None) -> pd.DataFrame:
    if not isinstance(df_oi, pd.DataFrame):
        df_oi = pd.read_excel(fr"{os.environ['OneDrive']}\Publico\NYCOLAS\01 - PROJETOS\Automacao Spring Control\Logs\OI_DET_{mesref}.xlsx",  # noqa
                              decimal=',',
                              sheet_name='Sheet1',
                              dtype=str)

    df_oi['ORIGEM'] = df_oi['ORIGEM'].fillna('nan')
    df_oi['aux'] = np.where(df_oi['ORIGEM'] == 'nan', df_oi['CONTA'], df_oi['ORIGEM'])  # noqa
    df_oi['aux'] = (df_oi['aux']
                    .str.replace('-', '')
                    .str.replace('_', '')
                    .str.replace(' ', ''))

    return df_oi


def __merge_dfs(df_oi: pd.DataFrame, df_desig: pd.DataFrame) -> pd.DataFrame:
    # Fazendo uma cópia explícita de df_desig
    # para evitar o SettingWithCopyWarning
    df_desig = df_desig.copy()

    # Para realizar o merge, adicione uma coluna correspondente em df_desig
    df_desig['aux'] = df_desig.apply(
        lambda row:
            row['designacao']
            if row['designacao'] in df_oi['aux'].values
            else row['fat_fatura'],
        axis=1)

    df_oi['aux'] = df_oi['aux'].astype(str)
    df_desig['aux'] = df_desig['aux'].astype(str)

    df_merged = df_oi.merge(df_desig, how='left', on='aux')

    df_merged.columns = df_merged.columns.str.upper()

    df_merged['CDC'] = np.where(df_merged['ORIGEM'].isna(), df_merged['FAT_CDC'], df_merged['DESIG_CDC'])  # noqa
    df_merged['FILIAL'] = np.where(df_merged['ORIGEM'].isna(), df_merged['FAT_FILIAL'], df_merged['DESIG_FILIAL'])  # noqa
    df_merged['OBSERVACAO'] = np.where(df_merged['ORIGEM'].isna(), df_merged['FAT_OBSERVACOES'], df_merged['DESIG_OBSERVACOES'])  # noqa
    df_merged['ENTREGUE'] = dt.now().strftime('%d/%m/%Y')

    df_merged['VALOR_PDF'] = df_merged['VALOR_PDF'].apply(
        lambda x: locale.currency(float(str(x).replace(',', '.')), grouping=True, symbol="R$")
    )

    df_merged['VALOR_DET'] = df_merged['VALOR_DET'].fillna(0.0)
    df_merged['VALOR_DET'] = df_merged['VALOR_DET'].apply(
        lambda x: locale.currency(float(str(x).replace(',', '.')), grouping=True, symbol="R$")
    )

    return df_merged


def __treat_df(df_merged: pd.DataFrame) -> pd.DataFrame:
    # Filtrando as colunas
    df_final = df_merged[[
        'OPERADORA',
        'MESREF',
        'CONTA',
        'FATURA',
        'EMISSAO',
        # 'TIPO',
        'ORIGEM',
        'DESCRICAO',
        'VALOR_PDF',
        'VALOR_DET',
        'VENCIMENTO',
        'CDC',
        'FILIAL',
        'ENTREGUE',
        'OBSERVACAO'
    ]].copy()  # Fazendo uma cópia explícita para evitar SettingWithCopyWarning

    df_final.rename(columns={
        'OPERADORA': 'Fornecedor',
        'MESREF': 'Ref.',
        'CONTA': 'Conta',
        'FATURA': 'Num. Doc.',
        'EMISSAO': 'Emissão',
        # 'TIPO': '',
        'ORIGEM': 'Designação',
        'DESCRICAO': 'Descrição',
        'VALOR_PDF': 'Valor',
        'VALOR_DET': 'Rateio',
        'VENCIMENTO': 'Vencimento',
        'CDC': 'Centro de Custo',
        'FILIAL': 'Filial',
        'ENTREGUE': 'Entregue',
        'OBSERVACAO': 'Observação'
    }, inplace=True)

    df_final.sort_values(by=['Vencimento', 'Conta', 'Designação'], inplace=True)

    df_final.reset_index(drop=True, inplace=True)

    __validade_df(df_final)

    df_final.fillna('', inplace=True)

    return df_final


def __validade_df(df_final: pd.DataFrame) -> pd.DataFrame:
    filter_df = df_final[df_final['Centro de Custo'].isna()]
    if not filter_df.empty:
        print(filter_df.to_markdown())
        raise ValueError('O dataframe gerado contém valores nulos na coluna "Centro de Custo"')


def __adjust_column_widths(writer, sheet_name):
    worksheet = writer.sheets[sheet_name]
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except Exception:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column].width = adjusted_width


def __export_to_excel(df_final: pd.DataFrame, mesref: str):
    css_alt_rows = 'background-color: lightgray; color: black;'
    css_indexes = 'background-color: black; color: white; font-weight: bold; text-align: center;'

    styled_df = (df_final.style.apply(
        lambda col: np.where(col.index % 2, css_alt_rows, None))
                 .map_index(lambda _: css_indexes, axis=0)
                 .map_index(lambda _: css_indexes, axis=1))

    file_path = f'Rateio_Oi_{mesref}.xlsx'
    writer = pd.ExcelWriter(file_path, engine='openpyxl')
    styled_df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Ajustando a largura das colunas
    __adjust_column_widths(writer, 'Sheet1')

    writer.close()


def get_rateio(mesref: str, df_oi: pd.DataFrame = None,
               export: bool = True) -> pd.DataFrame:
    db_faturas = ControlDatabases("faturas.db")

    df_desig = __get_desig(db_faturas)
    df_oi = __get_aux_df_oi(mesref, df_oi)
    df_merged = __merge_dfs(df_oi, df_desig)
    df_final = __treat_df(df_merged)

    if export:
        __export_to_excel(df_final, mesref)

    return df_final


if __name__ == '__main__':
    get_rateio(mesref='2024-07')
