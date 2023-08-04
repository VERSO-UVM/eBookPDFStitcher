import PyPDF2
import tkinter as tk
from tkinter import filedialog

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

    pdf_writer = PyPDF2.PdfWriter()

    for pdf_file in pdf_files:
        with open(os.path.join(input_folder, pdf_file), 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

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