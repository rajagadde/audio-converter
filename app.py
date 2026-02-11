import os
import uuid
import subprocess
from flask import Flask, render_template, request, send_file, redirect, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_FORMATS = ["mp3", "wav", "aac", "flac", "ogg", "mpeg", "m4a", "opus"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if "audio" not in request.files:
            flash("No file selected")
            return redirect("/")

        file = request.files["audio"]

        if file.filename == "":
            flash("No file selected")
            return redirect("/")

        output_format = request.form["format"]

        if output_format not in ALLOWED_FORMATS:
            flash("Invalid output format")
            return redirect("/")

        unique_name = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(input_path)

        output_path = f"{input_path}.{output_format}"

        try:
            command = [
                "ffmpeg",
                "-y",
                "-i", input_path,
                output_path
            ]
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            return send_file(output_path, as_attachment=True)

        except:
            flash("Conversion failed")
            return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
