from flask import Flask, request, render_template, send_file, make_response
import pdf_engine
import os
import shutil
import uuid

app = Flask(__name__)
upload = "uploaded_files"

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    if request.cookies.get('id') == None:
        id = str(uuid.uuid1())
        response.set_cookie('id', id)
    id = request.cookies.get('id')
    upload_dir = os.path.join(upload, id)
    if(not os.path.isdir(upload_dir)):
        os.mkdir(upload_dir)
    return response

@app.route("/", methods=["POST"])
def index_buttons():
    # to if we want to add more buttons I think you can just add another if statement for the action type and it should work!
    action = request.form.get("action")
    if action == "upload":
        files = request.files.getlist("file")
        # save each file in the uploaded_files folder
        # TODO: eventually move to static folder for embedding pdf viewing
        id = request.cookies.get('id')
        for i in files:
            i.save(f"{upload}/{id}/{i.filename}")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/file_settings", methods=["POST"])
def settings_buttons():
    id = request.cookies.get('id')
    input_directory = os.path.join(upload, id)
    file_name = request.form.get("file_name")
    try :
        output = pdf_engine.stitch_pdf(input_directory=input_directory, document_name = file_name)
        shutil.rmtree(input_directory)
        return send_file(output, as_attachment=True)
    except Exception as e : 
        return render_template("index.html")
    
@app.route("/acknowledgement")
def acknowledgement():
    return render_template ("acknowledgement.html")