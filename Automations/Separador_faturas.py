import os
import traceback
import _main_path
import fastparquet
import pandas as pd

from os.path import join
from datetime import datetime as dt

from Objects.Obj_PDF_Reader import PDFReader

_main_path.__loader__
fastparquet.__loader__


def read_log(path: str,
             file: str,
             engine: str = 'fastparquet') -> pd.DataFrame:
    path_file = join(path, file+'.parquet')

    try:
        return pd.read_parquet(path_file, engine=engine)
    except Exception:
        if not os.path.exists(path):
            os.mkdir(path)

        return pd.DataFrame()


def write_log(path: str,
              file: str,
              df: pd.DataFrame,
              engine: str = 'fastparquet'):

    def file_base(formato):
        return join(path, file+'.'+formato)  # type: ignore

    df.to_parquet(file_base('parquet'), engine=engine)
    df.to_csv(file_base('csv'), sep=';')


def invoices_split(mesref: str = None) -> None:
    automation_path = join(
        os.environ['OneDrive'],
        r"Clientes\COMERCIAL\ICATU\GESTÃO\02 - AUTOMACOES")

    if not mesref:
        mesref = (dt.now()).strftime('%Y-%m')

    mesref = mesref.replace('/', '-')

    temp_path = join(automation_path, "TEMP")
    log_path = join(automation_path, "LOG")
    invoices_path = join(automation_path, "PARA TRATAR", mesref)

    if not os.path.exists(invoices_path):
        os.mkdir(invoices_path)

    readed_files = []

    files = os.listdir(temp_path)
    main_df = read_log(log_path, 'main_log')

    # Caso não exista um arquivo log, ele ignora.
    # Caso exista um arquivo log, ele filtra
    # a partir da data da var dt_init_search_df.
    if not main_df.empty:
        readed_files = main_df['file'].to_list()

    qtd_arquivos = len(files)
    print(f"Quantidade total de pdf's: {qtd_arquivos}")

    for i, f in enumerate(files):
        print(f'\nArquivo {i+1}/{qtd_arquivos}')
        if f in readed_files:
            print(f'O arquivo {f} já foi lido')
            os.remove(join(temp_path, f))
            continue

        obj_pdf = PDFReader(f, temp_path)

        engine = "fitz"  # PyPDF2 | fitz
        pdf = obj_pdf.read_pdf(engine)

        invoice_info = {
            "path": temp_path,
            "file": f,
            "cliente": None,
            "dt_download": dt.now().strftime('%d/%m/%Y %H:%M')
        }

        cliente = None
        print("Lendo o arquivo %s" % f)
        try:
            for pag in range(
                    len(pdf.pages)
                    if engine == "PyPDF2"
                    else pdf.page_count):

                # print("Numero da página:", pag+1)
                try:
                    page = obj_pdf.get_text(pdf, pag)

                except IndexError:
                    continue

                except TypeError:
                    continue

                if not cliente or cliente == "Desconhecido":
                    page_lower = page.lower()

                    if ("www2.embratel.com.br" in page_lower or
                            "www.embratel.com.br" in page_lower):
                        cliente = "EMBRATEL"

                    elif " net " in page_lower:
                        cliente = "NET"

                    elif " claro " in page_lower:
                        cliente = "CLARO"

                    elif " oi " in page_lower:
                        cliente = "OI"

                    elif " vivo " in page_lower or 'www.vivo.com.br' in page:
                        cliente = "VIVO"

                    elif "tim " in page_lower:
                        cliente = "TIM"

                    elif " gvt " in page_lower:
                        cliente = "GVT"

                    elif "algar " in page_lower:
                        cliente = "ALGAR"

                    else:
                        cliente = "Desconhecido"

                    invoice_info['cliente'] = cliente

                    if cliente and cliente != "Desconhecido":
                        print("Operadora: %s" % cliente)
                        obj_pdf.close_pdf()
                        if not os.path.exists(join(invoices_path, cliente)):
                            os.mkdir(join(invoices_path, cliente))

                        os.replace(
                            join(temp_path, f),
                            join(invoices_path, cliente, f)
                        )

                        invoice_info['path'] = join(invoices_path, cliente, f)

                        break

                # lines = page.split('\n')
                # for i, line in enumerate(lines):
                #     print(i, line, )

        except Exception:
            obj_pdf.close_pdf()
            traceback.print_exc()

        else:
            if cliente == "Desconhecido":
                obj_pdf.close_pdf()
                if not os.path.exists(join(invoices_path, cliente)):
                    os.mkdir(join(invoices_path, cliente))

                os.replace(
                    join(temp_path, f),
                    join(invoices_path, cliente, f)
                )

                invoice_info['path'] = join(invoices_path, cliente, f)

            df = pd.DataFrame.from_dict(
                [invoice_info],
                orient='columns')
            main_df = pd.concat([main_df, df])

    main_df.reset_index(drop=True, inplace=True)
    write_log(log_path, 'main_log', main_df)


if __name__ == '__main__':
    invoices_split('2024-04')
