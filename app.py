from flask import Flask, request, render_template
import os
import pdf_stitcher

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("file")
    # save each file in the uploaded_files folder
    for i in files:
        i.save(f"uploaded_files/{i.filename}")
    # go to the file settings page
    return render_template("file_settings.html")

@app.route("/file_settings")
def stitch_pdf():
    # make list 
    pdf_files = []
    for i in os.listdir("uploaded_files"):
        if i.endswith(".pdf"):
            pdf_files.append(os.path.join("uploaded_files", i))
    
    # Create a temporary directory in the output folder and define the path for the merged PDF file
    temp_dir = os.path.join("/output", "temp")
    os.makedirs(temp_dir, exist_ok=True)
    merged_pdf = os.path.join(temp_dir, "merged.pdf")

    # Merge the selected PDF files into a single PDF file
    pdf_stitcher.merge_pdfs(pdf_files, merged_pdf)
    
    # # Define the path for the renumbered PDF file
    renumbered_pdf = os.path.join(temp_dir, "renumbered.pdf")

    # # # Renumber the pages of the merged PDF file
    pdf_stitcher.renumber_pdf(merged_pdf, renumbered_pdf)
    
    # move merged pdf to output
    
    
    

    
