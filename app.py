from flask import Flask, request, render_template, send_file, make_response, redirect
import pdf_engine
import os
import shutil
import uuid

app = Flask(__name__)
upload = "uploaded_files"
app.secret_key = "Im_only_doing_this_for_flask"

@app.route("/")
def index():
    if request.cookies.get('id') == None:
        id = str(uuid.uuid1())
        response = make_response(redirect("/"))
        response.set_cookie('id', id)
        return response
    response = make_response(render_template("index.html"))
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
        #TODO We need to figure out why this error is happening
        return redirect("/acknowledgement")
    
@app.route("/file_settings")
def auto_stitch():
    id = request.cookies.get('id')
    user_directory = os.path.join(upload, id)
    stitch_dir = os.mkdir(os.path.join(user_directory,"stitched_pdfs"))
    pdf_engine.stitch_pdf(output_folder=stitch_dir,input_directory=user_directory,document_name="auto_stitched")

@app.route("/acknowledgement")
def acknowledgement():
    return render_template ("acknowledgement.html")

@app.route("/errors")
def errors():
    return render_template("errors.html")