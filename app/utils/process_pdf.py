import io

import fitz
from PIL import Image


class ProcessPDF:
    def __init__(self, file_path):
        self.file_path = file_path

    def split_pdf_into_images(self):
        pdf = fitz.open(self.file_path)
        images = []
        for i in range(pdf.page_count):
            page = pdf[i]
            if page.get_text() == '':
                pixmap = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            else:
                pixmap = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='JPEG')
            byte_arr = byte_arr.getvalue()
            images.append(byte_arr)
        pdf.close()
        return images