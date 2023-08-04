import PyPDF2
import os

def stitch_pdfs(input_folder, output_filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_folder_path = os.path.join(script_directory, input_folder)

    # Get a list of all PDF files in the input folder
    pdf_files = [file for file in os.listdir(input_folder_path) if file.endswith('.pdf')]
    pdf_files.sort()  # Sort files in alphabetical order (you can modify the sorting order as needed)

    # Create a PDF writer object to hold the combined PDF pages
    pdf_writer = PyPDF2.PdfWriter()

    # Loop through each PDF file and add its pages to the writer
    for pdf_file in pdf_files:
        with open(os.path.join(input_folder_path, pdf_file), 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)  # Use num_pages method to get the number of pages
            for page_num in range(num_pages):
                page = pdf_reader._get_page(page_num)  # Use get_page method to access pages
                pdf_writer.add_page(page)


    # Save the combined PDF to a new file
    with open(output_filename, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Successfully stitched {len(pdf_files)} PDFs into '{output_filename}'.")

# Usage example
if __name__ == "__main__":
    input_folder = "pdf_files"
    output_filename = "combined_output.pdf"
    stitch_pdfs(input_folder, output_filename)