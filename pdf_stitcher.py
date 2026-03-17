import PySimpleGUI as sg
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
        # Renumber the page
        pdf_doc[page_num].get_text("Page {}".format(page_num + 1))

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
    for page_num in range(pdf_reader.getNumPages()):
        # If the page is not in the list of pages to delete, add it to the PdfWriter object
        if page_num not in pages_to_delete:
            pdf_writer.add_page(pdf_reader.getPage(page_num))

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

# This function displays a preview of the PDF file with options to delete or save pages
def show_preview(pdf_file, output_folder, document_name):
    """
    Display a preview of the PDF with options to delete or save pages.

    Parameters:
    - pdf_file (str): The path to the input PDF file.
    - output_folder (str): The path to the output folder.
    - document_name (str): The name of the document.

    """
    # This function updates the preview window
    def update_preview(window, current_page, temp_filenames, total_pages):
       # Update the image and page number
       window["-IMAGE-"].update(filename=temp_filenames[current_page])
       window["-PAGE-"].update(f"Page {current_page + 1} of {total_pages}")
    
    # Open the PDF file and get the total number of pages
    pdf_doc = fitz.open(pdf_file)
    total_pages = len(pdf_doc)

    
    # use directory with easy access like desktop
    temp_dir = tempfile.mkdtemp(suffix=".pdf", prefix="pdf_temp_")
    temp_filenames = [os.path.join(temp_dir, f"temp_page_{i}.png") for i in range(total_pages)]


    # Save previews for all pages
    for page_num in range(total_pages):
        # Save a preview of the page
        pdf_doc[page_num].get_pixmap().save(temp_filenames[page_num], output="png", jpg_quality=95)

    # Define the layout of the preview window
    layout = [
        [sg.Image(filename=temp_filenames[0], key="-IMAGE-")],
        [sg.Text(f"Page 1 of {total_pages}", key="-PAGE-")],
        [sg.Text("Pages to delete (comma-separated):"), sg.InputText(key="-PAGES-")],
        [sg.Button("Delete Pages"), sg.Button("Save Pages"), sg.Button("Exit")],
    ]

    # Create the preview window
    window = sg.Window("PDF Merger Preview", layout, finalize=True)

    # Initialize the current page
    current_page = 0

    # Event loop for the preview window
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        if event == "Delete Pages":
            pages_to_delete = [page.strip() for page in values["-PAGES-"].split(",") if page.strip()]
            invalid_pages = [page for page in pages_to_delete if not page.isdigit()]

            if invalid_pages:
                sg.popup_error(f"Invalid page(s): {', '.join(invalid_pages)}")
                continue

            pages_to_delete = [int(page) for page in pages_to_delete]
            
            if pages_to_delete:
                # Remove pages from the list of temp filenames
                temp_filenames = [temp_filenames[i] for i in range(total_pages) if i not in pages_to_delete]
            
            # Update total_pages after deletion
            total_pages = len(temp_filenames)

            # Handle the case where deleting pages results in an empty list
            if not temp_filenames:
                current_page = 0
                break
            else:
                # Update current_page if needed
                if current_page >= total_pages:
                    current_page = total_pages - 1

                update_preview(window, current_page, temp_filenames, total_pages)
                sg.popup(f"Page(s) {', '.join(map(str, pages_to_delete))} deleted!", title="Page(s) Deleted")


            # Draw image on canvas after deletion
            img_data = sg.Image(filename=temp_filenames[current_page])
            # canvas.draw_image(data=img_data, location=(0, 600))

        elif event == "Save Pages":
            save_pages = [int(page.strip()) for page in values["-PAGES-"].split(",") if page.strip()]
            
            if save_pages:
                remaining_pdf = os.path.join(output_folder, f"{document_name}.pdf")
                save_remaining_pages(pdf_file, remaining_pdf, save_pages)
                sg.popup("Remaining pages saved!", f"Output saved as 'remaining.pdf' in {output_folder}")

    window.close()

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_dir)

def main():
    # Get user input for the document name using a pop-up dialog
    document_name = sg.popup_get_text("Enter document name:")

    # Check if the document name is provided; if not, show an error and exit
    if not document_name:
        sg.popup("Document name cannot be empty. Exiting.")
        return
    
    # Get a list of PDF files to merge using a pop-up dialog
    pdf_files = sg.popup_get_file("Select PDF files to merge", multiple_files=True, file_types=(("PDF Files", "*.pdf"),))

    # Check if no PDF files are selected; if so, show an error and exit
    if not pdf_files:
        sg.popup("No files selected. Exiting.")
        return

    # Get the output folder for the merged PDF using a pop-up dialog
    output_folder = sg.popup_get_folder("Select the output folder")

    # Check if no output folder is selected; if so, show an error and exit
    if not output_folder:
        sg.popup("No output folder selected. Exiting.")
        return
    
   # Create a temporary directory in the output folder and define the path for the merged PDF file
    temp_dir = os.path.join(output_folder, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    merged_pdf = os.path.join(temp_dir, "merged.pdf")

    # Merge the selected PDF files into a single PDF file
    merge_pdfs(pdf_files, merged_pdf)
    
    # Define the path for the renumbered PDF file
    renumbered_pdf = os.path.join(temp_dir, "renumbered.pdf")

    # Renumber the pages of the merged PDF file
    renumber_pdf(merged_pdf, renumbered_pdf)
    
    # Initialize an empty list for pages to delete
    pages_to_delete = []

    # Show a preview of the renumbered PDF file and allow users to delete or save pages
    show_preview(renumbered_pdf, output_folder, document_name)

    # Define the final output path for the PDF file after deletion
    final_output_pdf = os.path.join(output_folder, f"{document_name}.pdf")
    
    # Delete specified pages from the renumbered PDF file and show a confirmation pop-up
    delete_pages(renumbered_pdf, pages_to_delete, final_output_pdf)
    sg.popup("Pages deleted!", f"Output saved as '{document_name}.pdf' in {output_folder}")

# Open and close the file using a with statement
    with fitz.open(renumbered_pdf) as pdf:
        pass  # Do nothing, just open and close the file 

    # Remove the temporary directory and its contents
    shutil.rmtree(temp_dir)

# Main function call
if __name__ == "__main__":
    main()
