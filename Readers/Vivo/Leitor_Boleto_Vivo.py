import locale
import os
from datetime import datetime as dt
from os.path import join

import pandas as pd

import _main_path
from Objects.Obj_Invoice import Invoice
from Objects.Obj_PDF_Reader import PDFReader

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def __get_info_fixo__(invoice: Invoice, page: str):
    lines = page.split('\n')
    for i, line in enumerate(lines):
        print(i, line.strip())

        if not invoice.designacao:
            if "TELEFONE(S)" in line:
                invoice.designacao = lines[i+1]

        if not invoice.valor:
            if "Valor a pagar" in line:
                invoice.valor = lines[i+1]

        if not invoice.conta:
            if "Código do cliente" in line:
                invoice.conta = lines[i+1]
                invoice.conta = invoice.conta.replace(' DV: ', '-')
                while ' -' in invoice.conta:
                    invoice.conta = invoice.conta.replace(' -', '-')

        if not invoice.fatura:
            if "Número da fatura" in line:
                invoice.fatura = lines[i+1]

        # if not invoice.servicos:
            # if "" in line:
            #     invoice.servicos = lines[i+1] + lines[i+2] + lines[i+3]

        if not invoice.cnpj:
            if "CNPJ / CPF" in line:
                invoice.cnpj = lines[i+1]

        if not invoice.emissao:
            if "Data de emissão" in line:
                invoice.emissao = lines[i+1]

        if not invoice.vencimento:
            if "Data de vencimento " in line or 'Vencimento: ' in line:
                invoice.vencimento = line.split()[-1]

        if not invoice.mesref:
            if "Mês de referência" in line:
                invoice.mesref = lines[i+1]


def __get_info_movel__(invoice: Invoice, page: str):
    lines = page.split('\n')
    for i, line in enumerate(lines):
        # print(i, line.strip())

        if not invoice.valor:  # ok
            if "Total a Pagar - R$" in line:
                invoice.valor = lines[i+2]

        if not invoice.conta:  # ok
            if "Nº da Conta" in line:
                invoice.conta = lines[i+1]

        if not invoice.fatura:  # ok
            if "Cód. Débito Automático" in line:
                invoice.fatura = lines[i+1]

        # if not invoice.servicos:
            # if "" in line:
            #     invoice.servicos = lines[i+1] + lines[i+2] + lines[i+3]

        if not invoice.emissao:  # ok
            if "Data de emissão: " in line:
                invoice.emissao = line.strip().split()[-1]

        if not invoice.vencimento:  # ok
            if "Vencimento" in line:
                invoice.vencimento = lines[i+2]

        if not invoice.mesref:  # ok
            if "Mês Referência" in line:
                invoice.mesref = lines[i+1]
                invoice.mesref = dt.strptime(invoice.mesref, '%m/%Y')
                invoice.mesref = invoice.mesref.strftime("%B/%Y").capitalize()


_main_path.__loader__
mesref = dt.now().strftime('%Y-%m')

invoices_path = join(
    os.environ['OneDrive'],
    r"Clientes\COMERCIAL\ICATU\GESTÃO\02 - AUTOMACOES\PARA TRATAR",
    mesref,
    "VIVO")

files = os.listdir(invoices_path)

main_df = pd.DataFrame()

for f in files[-1:]:
    print(f"Lendo o arquivo {f}...")
    obj_pdf = PDFReader(f, invoices_path)
    invoice = Invoice()

    # engine = "PyPDF2"  # PyPDF2 | fitz
    engine = "fitz"  # PyPDF2 | fitz
    pdf = obj_pdf.read_pdf(engine)

    invoice.operadora = "Vivo"
    invoice.arquivo = f
    invoice.cnpj = None
    invoice.tipo = None

    list_services = []
    num_fatura = None
    try:
        for pag in range(len(pdf.pages) if engine == "PyPDF2"
                         else pdf.page_count):

            # print("Numero da página:", pag+1)
            page = obj_pdf.get_text(pdf, pag)

            if not invoice.tipo:
                if 'Seu Demonstrativo de Despesas' in page:
                    invoice.tipo = "fixo"

                else:
                    invoice.tipo = "movel"

            if invoice.tipo == "fixo":
                __get_info_fixo__(invoice, page)

            else:
                __get_info_movel__(invoice, page)

    except Exception:
        print(f"Falha ao ler o arquivo {f}")
        raise

    else:
        if invoice.designacao:
            designacoes = invoice.designacao.split(',')
            if len(designacoes) > 1:
                invoice.valor = 'rateio'
            for d in designacoes:
                temp_invoice = invoice
                temp_invoice.designacao = str(d).strip()
                main_df = pd.concat([main_df, temp_invoice.create_dataframe()])

        else:
            main_df = pd.concat([main_df, invoice.create_dataframe()])

    finally:
        obj_pdf.close_pdf()

print(main_df)
main_df.to_csv('Logs/vivo_files.csv', sep=';', index=False, encoding='utf-8')
