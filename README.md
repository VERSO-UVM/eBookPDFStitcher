# eBookPDFStitcher

## Summary
This project came from a request by the Library to create a simple application that can stitch together pdfs. Publishers will often publish a book with each chapters in seperate PDF documents, in order to make the digital copy of the book lendable the Library need to be able to stictch together a sequence of PDFs into a single PDF. Currently the workaround requires expensive software and requires expertise in that software.

## Project History
The first version is a simple python script that has a basic user interface which allows you to select a folder (it assumes the file names are in decending order) and then allows you to select a place to save the combined file. Once selected it will stitch all the files together. This was demoed for the primary user and they liked the approach and wanted it in a chrome extension or some application that they can run when they need to.

## Example PDfs
Youi can find in the UVM Library catalog by searching “JSTOR Books”, for example:

https://www.jstor.org/stable/j.ctt7zsx4h (included as Book 1)
https://www.jstor.org/stable/j.ctt3fhx5m (included as Book 2)
https://www.jstor.org/stable/j.ctt2jcq33
https://www.jstor.org/stable/j.ctt4cgmp0
 
## Known Complications
- It is not clear how often the chapters have a numeric numbers that allows automatic ordering to happen. Most likely there needs to be a way to put the files in order
- The python PDf library noted that if page sizes are different it can have problems, there may need to be a check for that

# Dependencies
To run the current python script you can use the PyPDF2 library in Python. If you haven't installed it yet, you can do so using pip:

pip install PyPDF2

## Answered FAQ
Do the books tend to stick to a similar layout, or does it vary from one book to another? For instance, do they typically include elements like title pages and page numbers in consistent locations, or is it more diverse?
*Layouts vary some, but almost all books will have a title page and page numbers in consistent locations.*

Do the dimensions of the pdfs often vary between chapters (so from a letter to a legal size) in a set of scans?
*All books are consistent chapter to chapter.*

Is there a max number of individual PDF chapters for a given book the tool will need to handle and merge?
*Rare to see an academic book with more than 50 chapters*
