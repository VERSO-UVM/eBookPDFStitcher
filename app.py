from flask import Flask, request, render_template, send_file, make_response, redirect, flash, session, send_from_directory
from flask_session import Session
from cachelib.file import FileSystemCache
from datetime import  timedelta
import pdf_engine
import os
import shutil
import uuid
import format_converter
import subprocess

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
    if(os.path.isdir(upload_dir)):
        shutil.rmtree(upload_dir)
    os.mkdir(upload_dir)
    return response

@app.route("/", methods=["POST"])
def index_buttons():
    # to if we want to add more buttons I think you can just add another if statement for the action type and it should work!
    action = request.form.get("action")
    if action == "upload":
        files = request.files.getlist("file")
        
        id = session.get('id')
        user_directory = f"{upload}/{id}"
        
        # start gotenberg with docker
        subprocess.Popen([
            "docker", "run", "--rm",
            "-p", "3000:3000",
            "gotenberg/gotenberg:8"
        ])
        
        for i in files:
            i.save(os.path.join(user_directory, i.filename))
            
            ext = os.path.splitext(i.filename)[1]
            if ext != ".pdf":
                converted_path = pdf_engine.convert_to_pdf(f"{user_directory}/{i.filename}",False)

                   
        # make directory with autostitched pdf for preview purposes 
        stitch_dir = f"{user_directory}/stitched_pdfs"
        os.makedirs(stitch_dir, exist_ok=True)
        pdf_engine.stitch_pdf(output_folder=stitch_dir,input_directory=user_directory,document_name="auto_stitched")
        # go to the file settings page
        return render_template("file_settings.html")


@app.route("/download_pdf", methods=["POST"])
def settings_buttons():
    id = session.get('id')
    user_directory = os.path.join(upload, id)
    stitched_pdf_dir = os.path.join(user_directory,"stitched_pdfs")
    data = request.get_json()
    file_name = data.get("file_name") or "unnamed"

    try:
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
        response = make_response(send_from_directory(user_dir, filename))
    elif os.path.exists(os.path.join(output_dir, filename)):
        response = make_response(send_from_directory(output_dir, filename))
    else:
        raise FileNotFoundError(f"File \"{filename}\" not found")

    # make sure file isnt cashed so the preview updates every time
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/getInputList")
def get_file_list():
    id = session.get("id")
    user_dir = os.path.join('uploaded_files', id)
    file_list = []
    pdf_files = pdf_engine.get_pdf_files(user_dir)
    for pdf in pdf_files:
        info = pdf_engine.get_pdf_info(pdf)
        if info is not None:
            file_list.append(info)
    return file_list

@app.route("/restitch", methods=["POST"])
def restitch_preview():
    id = session.get('id')
    user_directory = os.path.join('uploaded_files', id)
    stitched_dir = os.path.join(user_directory,"stitched_pdfs")
    
    data = request.get_json()
    deleted_pages = data.get("deleted_pages") or []
    renumber = data.get("renumber", False)
    local_ordering = data.get("local_ordering") or []
    
    return pdf_engine.stitch_pdf(output_folder=stitched_dir,input_directory=user_directory,document_name="auto_stitched",pages_to_delete=deleted_pages,renumber = renumber,file_reorder=local_ordering)
