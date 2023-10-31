# Import necessary libraries
import pypdf as pypdf  # Import the pypdf library for PDF handling
import tkinter as tk  # Import the tkinter library for GUI
from tkinter import filedialog  # Import filedialog module from tkinter for file dialogs
import os  # Import the os module for operating system functions

# Function to combine PDFs
def combine_pdfs():
    # Prompt the user to select the input folder containing PDFs
    input_folder = filedialog.askdirectory(title="Select the folder with the PDFs")
    if not input_folder:  # If no folder is selected, return
        return

    # Prompt the user to select the output file location and name
    output_file = filedialog.asksaveasfilename(title="Select the output file location",
                                               defaultextension=".pdf",
                                               filetypes=[("PDF files", "*.pdf")])
    if not output_file:  # If no output file is selected, return
        return

    # Get a list of PDF files in the input folder and sort them
    pdf_files = [file for file in os.listdir(input_folder) if file.endswith('.pdf')]
    pdf_files.sort()

    # Create a PdfWriter object to combine PDFs
    pdf_writer = pypdf.PdfWriter()

    # Loop through each PDF file and its pages to add them to the PdfWriter
    for pdf_file in pdf_files:
        with open(os.path.join(input_folder, pdf_file), 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    # Write the combined PDF to the output file
    with open(output_file, 'wb') as output_file:
        pdf_writer.write(output_file)

    # Print a success message with the number of PDFs combined and the output file name
    print(f"Successfully stitched {len(pdf_files)} PDFs into '{output_file}'.")

# Main function to create the GUI and execute the PDF combiner
def main():
    # Create a root window for the GUI
    root = tk.Tk()
    root.title("PDF Combiner")  # Set the title of the window
    root.config(bg="green")
    root.minsize(200, 200)

    app_frame = tk.Frame(root, width=200, height=200)
    

    # Create a button to run the PDF combiner function
    run_button = tk.Button(root, text="Run PDF Combiner", command=combine_pdfs)
    run_button.pack(pady=110)  # Add padding to the button

    root.mainloop()  # Start the GUI event loop

# Entry point of the program
if __name__ == "__main__":
    main()  # Call the main function to start the program