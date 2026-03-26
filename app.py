from flask import Flask, request, render_template, send_file, make_response, redirect, flash, session, send_from_directory
from flask_session import Session
from cachelib.file import FileSystemCache
from datetime import  timedelta
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
        user_directory = f"{upload}/{id}"
        
        for i in files:
            i.save(f"{user_directory}/{i.filename}")   
        
        # make directory with autostitched pdf for preview purposes 
        stitch_dir = f"{user_directory}/stitched_pdfs"
        os.makedirs(stitch_dir, exist_ok=True)
        pdf_engine.stitch_pdf(output_folder=stitch_dir,input_directory=user_directory,document_name="auto_stitched")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/file_settings", methods=["POST"])
def settings_buttons():
    id = session.get('id')
    user_directory = os.path.join(upload, id)
    stitched_pdf_dir = os.path.join(user_directory,"stitched_pdfs") 
    file_name = request.form.get("file_name")
    
    try :
        duplicate = shutil.copy(f"{stitched_pdf_dir}/auto_stitched.pdf",f"output/{file_name}.pdf")
        shutil.rmtree(user_directory)
        return send_file(duplicate, as_attachment=True)
    except FileNotFoundError as e : 
        return redirect("/")
    except PermissionError as e:
        error = e 
        print(e)
        #TODO We need to figure out why this error is happening
        flash("we dont know why this is happening but it's linked to permision")
        return render_template("errors.html" , error = error)
    
@app.route("/no_more_times")
def remove_idle_user():
    id = session.get('id')
    user_directory = os.path.join(upload, id)
    try :
        shutil.rmtree(user_directory)
        return render_template("no_more_time.html")
    except Exception as e :
        print(e)
        return render_template("index.html")
    
@app.route("/acknowledgement")
def acknowledgement():
    return render_template ("acknowledgement.html")

@app.route("/errors")
def errors():
    return render_template("errors.html")

# allow JS to access only the output files and user id folder.
@app.route('/files/<path:filename>')
def serve_file(filename):
    id = session.get("id")

    user_dir = os.path.join('uploaded_files', id)
    output_dir = 'output'

    if os.path.exists(os.path.join(user_dir, filename)):
        return send_from_directory(user_dir, filename)
    elif os.path.exists(os.path.join(output_dir, filename)):
        return send_from_directory(output_dir, filename)
    else:
        raise FileNotFoundError(f"File \"{filename}\" not found")

@app.route("/getInputList")
def get_file_list():
    id = session.get("id")
    user_dir = os.path.join('uploaded_files', id)
    file_list = []
    pdf_files = pdf_engine.get_pdf_files(user_dir)
    for pdf in pdf_files:
        file_list.append(pdf_engine.get_pdf_info(pdf))
    return file_list