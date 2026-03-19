from flask import Flask, request, render_template, send_file

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

# @app.route("/name", method =["POST"])
# def download_file(name):
    




