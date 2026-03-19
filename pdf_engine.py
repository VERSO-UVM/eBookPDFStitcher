
from PyPDF2 import PdfReader, PdfWriter, PdfFileReader
import fitz
import os
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
        
        
def stitch_pdf(output_folder = "output", input_direcotry = "uploaded_files", document_name = None, pages_to_delete = [], remove_unstitched = False):
    """Merges, renumbers, and optionally cleans up a collection of PDF files.
    Parameters:
        output_folder (str): Path to the directory where the final PDF will be
            saved. Defaults to "output".
        input_direcotry (str): Path to the directory containing the input PDF
            files to stitch. Defaults to "uploaded_files".
        document_name (str, optional): Base name for the output PDF file
            (without extension). If None, defaults to "<n>_stitched" where
            <n> is the number of input files.
        pages_to_delete (list[int]): List of page numbers to remove from the
            merged PDF before saving. Defaults to [].
        remove_unstitched (bool): If True, deletes the input directory and its
            contents after stitching. Defaults to False.
    Returns:
        Stitched PDF
    """
    pdf_files = []
    # get all files from input directory
    for file in os.listdir(input_direcotry):
        pdf_files.append(os.path.join("uploaded_files", file))
        print(file)
    
    # if no document name is provided, default to a summary
    if not document_name:
        document_name = f"{len(pdf_files)}_stitched"
    
    temp_dir = os.path.join(output_folder, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    merged_pdf = os.path.join(temp_dir, "merged.pdf")

    # Merge the selected PDF files into a single PDF file
    merge_pdfs(";".join(pdf_files), merged_pdf)
    
    # # Define the path for the renumbered PDF file
    renumbered_pdf = os.path.join(temp_dir, "renumbered.pdf")

    # # # Renumber the pages of the merged PDF file
    renumber_pdf(merged_pdf, renumbered_pdf)
    
    # Define the final output path for the PDF file after deletion
    final_output_pdf = os.path.join(output_folder, f"{document_name}.pdf")
    
    # Delete specified pages from the renumbered PDF file and show a confirmation pop-up
    delete_pages(renumbered_pdf, pages_to_delete, final_output_pdf)

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_dir)
    # Remove input files folder if specified
    if remove_unstitched:
        shutil.rmtree(input_direcotry) 
    return final_output_pdf
    

