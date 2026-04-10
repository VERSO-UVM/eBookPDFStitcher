import pypandoc

# TODO change the code in this file to a workable one
# Define input and output files
input_file = r"pdf_files\Cheat sheet.docx"
output_file = r"pdf_files\document.pdf"

output = pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)

if output == "":
    print(f"Successfully converted {input_file} to {output_file}")