# eBookPDFStitcher

## Summary
This project came from a request by the Library to create a simple application that can stitch together pdfs. Publishers will often publish a book with each chapters in seperate PDF documents, in order to make the digital copy of the book lendable the Library need to be able to stictch together a sequence of PDFs into a single PDF. Currently the workaround requires expensive software and requires expertise in that software.

## Project History
The first version is a simple python script that has a basic user interface which allows you to select a folder (it assumes the file names are in decending order) and then allows you to select a place to save the combined file. Once selected it will stitch all the files together. This was demoed for the primary user and they liked the approach and wanted it in a chrome extension or some application that they can run when they need to.

## Known Complications
- It is not clear how often the chapters have a numeric numbers that allows automatic ordering to happen. Most likely there needs to be a way to put the files in order
- The python PDf library noted that if page sizes are different it can have problems, there may need to be a check for that

# Dependencies
To run the current python script you can use the PyPDF2 library in Python. If you haven't installed it yet, you can do so using pip:

pip install PyPDF2

There are test files taken from a real online book with their original file names that can be used for testing, but this is a limited sample of potential files that could be tested.
