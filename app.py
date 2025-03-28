import os
from flask import Flask, render_template, request, url_for, redirect, send_file
import uuid

from werkzeug.utils import send_from_directory

app = Flask(__name__)



UPLOAD_FOLDER = r"C:\Users\asus\Links\pythonProject1\BackupFolder"  # Make sure this path is correct
app.config['BackupFolder'] = UPLOAD_FOLDER

# Ensure the folder exists at app startup, not during every upload request
if not os.path.exists(app.config['BackupFolder']):
    os.makedirs(app.config['BackupFolder'])
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            # Generate a unique filename to avoid overwriting
            filename = file.filename
            file_ext = os.path.splitext(filename)[1]  # Get file extension
            unique_filename = f"{uuid.uuid4()}{file_ext}"  # Add a unique identifier to the filename

            # Save the file with the unique name in the specified folder
            file.save(os.path.join(app.config['BackupFolder'], unique_filename))
            # Return success message and render the 'index.html' template
            return render_template("index.html", message="File successfully backed up! ✅")
            # return "File successfully backed up! ✅"
    return render_template("index.html")


@app.route('/files')
def view_files():
    """Route to display all files in the backup folder and allow downloading"""
    # List all files in the backup folder
    files = os.listdir(app.config['BackupFolder'])
    return render_template("files.html", files=files)

@app.route('/download/<filename>')
def download_file(filename):
    """Serve the file for download from the backup folder"""
    file_path = os.path.join(app.config['BackupFolder'], filename)
    return send_file(file_path, as_attachment=True)




if __name__ == "__main__":
    app.run(debug=True)
