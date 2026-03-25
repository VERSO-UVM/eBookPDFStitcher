from flask import Flask, request, render_template, send_file, make_response
import pdf_engine
import os
import shutil
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    if request.cookies.get('id') == None:
        id = uuid.uuid1()
        response.set_cookie('id', str(id))
    return response

@app.route("/", methods=["POST"])
def index_buttons():
    # to if we want to add more buttons I think you can just add another if statement for the action type and it should work!
    action = request.form.get("action")
    if action == "upload":
        files = request.files.getlist("file")
        # save each file in the uploaded_files folder
        #TODO update this to make this so it's not just the file in the upload 
        for i in files:
            i.save(f"uploaded_files/{i.filename}")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/file_settings", methods=["POST"])
def settings_buttons():
    action = request.form.get("action")
    file_name = request.form.get("file_name")
    if action == "stitch":
        download = True
        output = pdf_engine.stitch_pdf(document_name = file_name)
        if download:
            return send_file(output, as_attachment=True)





