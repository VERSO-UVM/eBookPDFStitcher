from flask import Flask, request, render_template, send_file, make_response, redirect, flash, session
from flask_session import Session
from cachelib.file import FileSystemCache
from datetime import timedelta
import pdf_engine
import os
import shutil
import uuid

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'cachelib'
app.config['SESSION_SERIALIZATION_FORMAT'] = 'json'
# threshold represents number of session files it will keep track of at once before deleting old ones
app.config['SESSION_CACHELIB'] = FileSystemCache(threshold=20, cache_dir="static/session_info")
Session(app)

upload = "uploaded_files"
app.secret_key = "Im_only_doing_this_for_flask"


@app.route("/")
def index():
    if(session.get("id") == None):
        id = str(uuid.uuid1())
        session['id'] = id
        return redirect("/")
    response = make_response(render_template("index.html"))
    id = session.get('id')
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
        id = session.get('id')
        for i in files:
            i.save(f"{upload}/{id}/{i.filename}")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/file_settings", methods=["POST"])
def settings_buttons():
    id = session.get('id')
    user_directory = os.path.join(upload, id)
    stitched_pdf_dir = os.path.join(user_directory,"stitched_pdfs") 
    file_name = request.form.get("file_name")
    
    try :
        duplicate = shutil.copy(os.join(stitched_pdf_dir,"auto_stitched.pdf"),os.join("output",file_name))
        shutil.rmtree(user_directory)
        return send_file(duplicate, as_attachment=True)
    except FileNotFoundError as e : 
        return redirect("/")
    except PermissionError as e:
        error = e 
        #TODO We need to figure out why this error is happening
        flash("we dont know why this is happening but it's linked to permision")
        return render_template("errors.html" , error = error)
    
@app.route("/file_settings")
def auto_stitch():
    id = session.get('id')
    user_directory = os.path.join(upload, id)
    stitch_dir = os.mkdir(os.path.join(user_directory,"stitched_pdfs"))
    pdf_engine.stitch_pdf(output_folder=stitch_dir,input_directory=user_directory,document_name="auto_stitched")

@app.route("/acknowledgement")
def acknowledgement():
    return render_template ("acknowledgement.html")

@app.route("/errors")
def errors():
    return render_template("errors.html")