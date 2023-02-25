import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfFileReader, PdfFileWriter

class PDFStampApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Stamp App")
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        
        self.stamp_path = ""
        self.stamp_coords = (0, 0, 0, 0)
        self.input_paths = []
        self.output_folder_path = ""
        
        self.stamp_preview_label = tk.Label(self.master, text="No stamp selected", font=("Arial", 10))
        self.stamp_preview_label.pack(pady=10)
        
        choose_stamp_button = tk.Button(self.master, text="Choose Stamp", command=self.choose_stamp)
        choose_stamp_button.pack()
        
        choose_files_button = tk.Button(self.master, text="Choose Files", command=self.choose_files)
        choose_files_button.pack()
        
        choose_output_folder_button = tk.Button(self.master, text="Choose Output Folder", command=self.choose_output_folder)
        choose_output_folder_button.pack()
        
        stamp_files_button = tk.Button(self.master, text="Stamp Files", command=self.stamp_files)
        stamp_files_button.pack(pady=20)
        
    def choose_stamp(self):
        self.stamp_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.stamp_path:
            self.stamp_preview_label.configure(text="Selected stamp: {}".format(self.stamp_path.split("/")[-1]))
        else:
            self.stamp_preview_label.configure(text="No stamp selected")
        
    def choose_files(self):
        self.input_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not self.input_paths:
            messagebox.showwarning("No Files Selected", "You must select at least one input file.")
            
    def choose_output_folder(self):
        self.output_folder_path = filedialog.askdirectory()
        if not self.output_folder_path:
            messagebox.showwarning("No Output Folder Selected", "You must select an output folder.")
            
    def stamp_files(self):
        if not self.input_paths:
            messagebox.showwarning("No Files Selected", "You must select at least one input file.")
            return
        
        if not self.output_folder_path:
            messagebox.showwarning("No Output Folder Selected", "You must select an output folder.")
            return
        
        if not self.stamp_path:
            messagebox.showwarning("No Stamp Selected", "You must select a stamp.")
            return
        
        stamp_pdf = PdfFileReader(open(self.stamp_path, "rb")).getPage(0)
        
        for input_path in self.input_paths:
            with open(input_path, "rb") as input_file:
                input_pdf = PdfFileReader(input_file)
                output_pdf = PdfFileWriter()

                for i in range(input_pdf.getNumPages()):
                    page = input_pdf.getPage(i)
                    page.mergePage(stamp_pdf)
                    output_pdf.addPage(page)

                output_path = "{}/stamped_{}".format(self.output_folder_path, input_path.split("/")[-1])
                with open(output_path, "wb") as output_file:
                    output_pdf.write(output_file)
                    
        messagebox.showinfo("Stamping Complete", "All files have been stamped and saved to the output folder.")
        

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFStampApp(root)
    root.mainloop()
