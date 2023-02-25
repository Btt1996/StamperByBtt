import PyPDF2
import os

def add_stamp(pdf_path, stamp_path, x, y):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        pdf_writer = PyPDF2.PdfFileWriter()
        stamp_file = open(stamp_path, 'rb')
        stamp_pdf = PyPDF2.PdfFileReader(stamp_file)

        stamp_page = stamp_pdf.getPage(0)

        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            page.mergePage(stamp_page)
            pdf_writer.addPage(page)

        output_file_path = os.path.splitext(pdf_path)[0] + '_stamped.pdf'
        with open(output_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)

        stamp_file.close()

if __name__ == '__main__':
    add_stamp('example.pdf', 'stamp.pdf', 100, 100)
