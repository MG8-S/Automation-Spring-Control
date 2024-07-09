import os
import _main_path
import traceback
import pandas as pd

from os.path import join

from Objects.Obj_PDF_Reader import PDFReader
from Objects.Obj_Invoice import Invoice

_main_path.__loader__

mesref = "2024-05"

invoices_path = join(
    os.environ['OneDrive'],
    "Clientes/COMERCIAL/ICATU/GESTÃO/02 - AUTOMACOES/PARA TRATAR",
    mesref,
    "EMBRATEL")

files = os.listdir(invoices_path)

main_df = pd.DataFrame()

for f in files:
    print(f"Lendo o arquivo {f}...")
    obj_pdf = PDFReader(f, invoices_path)
    invoice = Invoice()

    engine = "fitz"  # PyPDF2 | fitz
    pdf = obj_pdf.read_pdf(engine)

    invoice.cliente = "Embratel"
    invoice.arquivo = f
    invoice.cnpj = None

    list_services = []
    num_fatura = None
    try:
        for pag in obj_pdf.get_pages():
            # print("Numero da página:", pag+1)
            page = obj_pdf.get_text(pdf, pag)
            lines = page.split('\n')
            for i, line in enumerate(lines):
                # print(i, line, )
                if not invoice.fatura:
                    invoice.fatura = obj_pdf.find_element(line, "Fatura :",
                                                          sep=":")

                if not invoice.emissao:
                    invoice.emissao = obj_pdf.find_element(line, "Emissão :")

                if (not invoice.vencimento
                   and "cimento" in line.lower()
                   and "Cedente" not in lines[i + 1]):
                    print(i, line, lines[i + 1])
                    invoice.vencimento = obj_pdf.find_element(line + lines[i + 1],
                                                              "../../....",
                                                              debug_line=True,
                                                              regex=True)[0]

                if not invoice.valor and "Total a Pagar" in line:
                    invoice.valor = obj_pdf.find_element(line + lines[i + 1] + lines[i + 2],
                                                         "[0-9]*,[0-9]{2}",
                                                         regex=True)[0]

                if not invoice.cnpj:
                    invoice.cnpj = obj_pdf.find_element(line, "CNPJ")

                if 'digo Cliente' in line and not invoice.conta:
                    invoice.conta = obj_pdf.find_element(lines[i + 1],
                                                         "[0-9]{10}-[0-9]{4}",
                                                         regex=True)[0]

    except Exception:
        traceback.print_exc()
    else:
        main_df = pd.concat([main_df, invoice.create_dataframe()])
    finally:
        obj_pdf.close_pdf()

print(main_df)
main_df.to_csv('logs/ebt_files.csv', sep=';')