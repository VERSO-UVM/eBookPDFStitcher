from flask import Flask, request, render_template, send_file
import pdf_engine
import os
import shutil

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def index_buttons():
    # to if we want to add more buttons I think you can just add another if statement for the action type and it should work!
    action = request.form.get("action")
    
    if action == "upload":
        files = request.files.getlist("file")
        # save each file in the uploaded_files folder
        for i in files:
            i.save(f"uploaded_files/{i.filename}")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/file_settings", methods=["POST"])
def settings_buttons():
    action = request.form.get("action")
    if action == "stitch":
        download = True
        output = pdf_engine.stitch_pdf()
        if download:
            return send_file(output, as_attachment=True)
    
    

    
# @app.route("/name", method =["POST"])
# def download_file(name):
    




