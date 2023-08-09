import pypdf as pypdf
import tkinter as tk
from tkinter import filedialog
import os

def combine_pdfs():
    input_folder = filedialog.askdirectory(title="Select the folder with the PDFs")
    if not input_folder:
        return

    output_file = filedialog.asksaveasfilename(title="Select the output file location",
                                               defaultextension=".pdf",
                                               filetypes=[("PDF files", "*.pdf")])
    if not output_file:
        return

    pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.pdf')]
    pdf_files.sort()

    pdf_writer = pypdf.PdfWriter()

    for pdf_file in pdf_files:
        with open(os.path.join(input_folder, pdf_file), 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    with open(output_file, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Successfully stitched {len(pdf_files)} PDFs into '{output_file}'.")

def main():
    root = tk.Tk()
    root.title("PDF Combiner")

    run_button = tk.Button(root, text="Run PDF Combiner", command=combine_pdfs)
    run_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()