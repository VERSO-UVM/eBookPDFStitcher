import pypandoc

#Take an input file and convert it to a pdf. Naming convention of the file dont really matter here 
#as long as it end in .pdf
def other_format_to_pdf(input_file):
    output_file = input_file  +".pdf"
    pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)


#TODO find a python library that allow this, as currently it would seem pypandoc does not allow conversion from pdf
def pdf_to_other_format(input_file,format):
    print("wip")
    # temp_name = input_file[:-4]
    # output_file = temp_name + "." +format
    # print(temp_name)
    # print(output_file)
    # print(input_file)
    # pypandoc.convert_file(input_file, format, outputfile=output_file)


if __name__ == "__main__":
    print("a")