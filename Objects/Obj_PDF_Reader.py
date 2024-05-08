import os
import re
import fitz

from PyPDF2 import PdfReader


class PDFReader:
    def __init__(self, file, path) -> None:
        self.file = file
        self.path = path

    def read_pdf(self, engine="PyPDF2"):
        self.engine = engine
        if engine not in ["PyPDF2", "fitz", "PyMuPDF"]:
            raise EnvironmentError("Engine não reconhecida. Engines disponiveis: PyPDF2, fitz, PyMuPDF")

        if engine == "PyPDF2":
            self.pdf_obj = open(os.path.join(self.path, self.file), 'rb',
                                encoding='utf-8')
            self.pdf_readed = PdfReader(self.pdf_obj)
            return self.pdf_readed

        elif engine == "fitz" or engine == "PyMuPDF":
            self.pdf_obj = fitz.open(os.path.join(self.path, self.file))
            return self.pdf_obj

    def get_text(self, pdf, page):
        if self.engine == "PyPDF2":
            return pdf.pages[page].extract_text()

        elif self.engine == "fitz" or self.engine == "PyMuPDF":
            return pdf.load_page(page).get_text()

    def find_element(self, line: str, element: str, index: int = -1,
                     sep: str = None, debug_line: bool = False,
                     regex: bool = None) -> str:
        if regex:
            result = re.findall(element, line)
            if len(result) > 0:
                return result

        if element in line:
            if debug_line:
                print(line)
                print(line.split(sep))

            found_element = line.split(sep)[index].strip()
            return found_element

    def close_pdf(self):
        self.pdf_obj.close()
        
    def __quit__(self):
        self.close_pdf()
