import pypandoc


def other_format_to_pdf(input_file):
    print(input_file)
    output_file = input_file  +".pdf"
    print(output_file)
    pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)


# if __name__ == "__main__":
# # TODO change the code in this file to a workable one
# # Define input and output files
#     # input_file = r"pdf_files\*.docx"
#     # output_file = r"pdf_files\document.pdf"

#     # output = pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)