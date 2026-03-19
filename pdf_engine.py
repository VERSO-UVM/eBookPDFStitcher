
from PyPDF2 import PdfReader, PdfWriter, PdfFileReader
import fitz
import os
import tempfile
import shutil

# This function merges multiple PDF files into a single PDF file
def merge_pdfs(pdf_files, output_file):
    """
    Merge multiple PDF files into a single PDF file.

    Parameters:
    - pdf_files (str): A string containing paths to PDF files separated by ';'.
    - output_file (str): The path to the output merged PDF file.

    """
    # Create a PdfWriter object
    pdf_merger = PdfWriter()

    # Loop through each PDF file
    for pdf_file in pdf_files.split(";"):
        # Open the PDF file
        with open(pdf_file, 'rb') as file:
            # Create a PdfReader object
            pdf_reader = PdfReader(file)

            # Loop through each page in the PDF file
            for page_num in range(len(pdf_reader.pages)):
                # Add the page to the PdfWriter object
                pdf_merger.add_page(pdf_reader.pages[page_num])

    # Write the merged PDF file to the output file
    with open(output_file, 'wb') as output:
        pdf_merger.write(output)
        
        
# This function renumbers the pages in a PDF file
def renumber_pdf(input_pdf, output_pdf):
    """
    Renumber pages in a PDF document.

    Parameters:
    - input_pdf (str): The path to the input PDF file.
    - output_pdf (str): The path to the output PDF file with renumbered pages.

    """
    # Open the PDF file
    pdf_doc = fitz.open(input_pdf)

    # Loop through each page in the PDF file
    for page_num in range(len(pdf_doc)):
        #Find the page to be renumbered 
        page = pdf_doc[page_num]
        #Since Python is 0 indexed, as to start as page 0 + 1
        text = f"Page {page_num + 1}"
        text_coords = (0, page.rect.height - 30)
        page.insert_text(text_coords, text)
        #pdf_doc[page_num].get_text("Page {}".format(page_num + 1))

    # Save the renumbered PDF file
    pdf_doc.save(output_pdf)
# This function deletes specified pages from a PDF file
def delete_pages(input_pdf, pages_to_delete, output_pdf):
    """
    Delete specified pages from a PDF document.

    Parameters:
    - input_pdf (str): The path to the input PDF file.
    - pages_to_delete (list): A list of page numbers to delete.
    - output_pdf (str): The path to the output PDF file after deleting pages.

    """
    # Create a PdfReader object
    pdf_reader = PdfReader(input_pdf)

    # Create a PdfWriter object
    pdf_writer = PdfWriter()



    # Loop through each page in the PDF file
    for page_num in range(len(pdf_reader.pages)):
        # If the page is not in the list of pages to delete, add it to the PdfWriter object
        if page_num not in pages_to_delete:
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the remaining pages to the output file
    with open(output_pdf, "wb") as output:
        pdf_writer.write(output)

# This function saves the remaining pages from multiple PDF files to a new PDF file
def save_remaining_pages(pdf_files, output_pdf, pages_to_save):
    """
    Save remaining pages from multiple PDF files to a new PDF.

    Parameters:
    - pdf_files (str): A string containing paths to PDF files separated by ';'.
    - output_pdf (str): The path to the output PDF file with saved pages.
    - pages_to_save (list): A list of page numbers to save.

    """
    # Create a PdfWriter object
    pdf_writer = PdfWriter()

    # Loop through each PDF file
    for pdf_file in pdf_files.split(";"):
        # Open the PDF file
        with open(pdf_file, 'rb') as file:
            # Create a PdfReader object
            pdf_reader = PdfReader(file)

            # Loop through each page in the PDF file
            for page_num in range(len(pdf_reader.pages)):
                # If the page is not in the list of pages to save, add it to the PdfWriter object
                if page_num not in pages_to_save:
                    pdf_writer.add_page(pdf_reader.pages[page_num])

    # Write the remaining pages to the oureaderput file
    with open(output_pdf, 'wb') as output:
        pdf_writer.write(output)

