import tkinter as tk
from tkinter import filedialog
import PyPDF2
import os

def select_pdf_file():
    global pdf_path
    pdf_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files", "*.pdf")])
    pdf_file_name_label.config(text=os.path.basename(pdf_path))
    return pdf_path

def select_folder():
    global output_path
    output_path = filedialog.askdirectory(title="Select Folder")
    output_folder_name_label.config(text=os.path.basename(output_path))
    return output_path

def apply_stamp():
    if not pdf_path or not output_path:
        return

    pdf_reader = PyPDF2.PdfFileReader(open(pdf_path, "rb"))
    pdf_writer = PyPDF2.PdfFileWriter()

    stamp_file_reader = PyPDF2.PdfFileReader(open(stamp_path, "rb"))
    stamp_page = stamp_file_reader.getPage(0)

    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        page.mergePage(stamp_page)
        pdf_writer.addPage(page)

    output_file_path = os.path.join(output_path, "stamped_" + os.path.basename(pdf_path))
    with open(output_file_path, "wb") as out_file:
        pdf_writer.write(out_file)

    output_file_name_label.config(text=os.path.basename(output_file_path))
    output_success_label.config(text="Stamp Applied Successfully!")

def choose_stamp():
    global stamp_path
    stamp_path = filedialog.askopenfilename(title="Choose Stamp", filetypes=[("PDF Files", "*.pdf")])
    stamp_file_name_label.config(text=os.path.basename(stamp_path))
    return stamp_path

window = tk.Tk()
window.title("PDF Stamper")

pdf_path = None
output_path = None
stamp_path = None

pdf_file_label = tk.Label(window, text="PDF File:")
pdf_file_label.grid(row=0, column=0)

pdf_file_name_label = tk.Label(window, text="")
pdf_file_name_label.grid(row=0, column=1)

pdf_select_button = tk.Button(window, text="Select PDF", command=select_pdf_file)
pdf_select_button.grid(row=0, column=2)

output_folder_label = tk.Label(window, text="Output Folder:")
output_folder_label.grid(row=1, column=0)

output_folder_name_label = tk.Label(window, text="")
output_folder_name_label.grid(row=1, column=1)

output_select_button = tk.Button(window, text="Select Folder", command=select_folder)
output_select_button.grid(row=1, column=2)

stamp_file_label = tk.Label(window, text="Stamp File:")
stamp_file_label.grid(row=2, column=0)

stamp_file_name_label = tk.Label(window, text="")
stamp_file_name_label.grid(row=2, column=1)

stamp_select_button = tk.Button(window, text="Choose Stamp", command=choose_stamp)
stamp_select_button.grid(row=2, column=2)

apply_stamp_button = tk.Button(window, text="Apply Stamp", command=apply_stamp)
apply_stamp_button.grid(row=3, column=1)

output_file_label = tk.Label(window, text="Output File:")
output_file_label.grid(row=4, column=0)

output_file_name_label = tk.Label(window, text="")
output_file_name_label.grid(row=4, column=1)

output_success_label = tk.Label(window, text="")
output_success_label.grid(row=5, column=1)

window.mainloop()
