import os
import uuid
import re
from flask import Flask, render_template, request, url_for, redirect, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = r"C:\Users\asus\Links\pythonProject1\BackupFolder"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt', 'jpg', 'png'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB limit

app.config['BackupFolder'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure the folder exists at app startup
if not os.path.exists(app.config['BackupFolder']):
    os.makedirs(app.config['BackupFolder'])


def sanitize_filename(filename):
    """
    Sanitize filename to remove potentially dangerous characters
    and ensure it's safe to use
    """
    # Remove non-alphanumeric characters except dots and underscores
    filename = re.sub(r'[^\w\.\-]', '_', filename)

    # Limit filename length
    filename = filename[:255]

    return filename


def generate_unique_filename(filename):
    """
    Generate a unique filename to prevent overwriting
    """
    # Sanitize the original filename
    safe_filename = sanitize_filename(filename)

    # Get file extension
    file_ext = os.path.splitext(safe_filename)[1]

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"

    return unique_filename


def allowed_file(filename):
    """
    Check if the file extension is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if file is present in the request
        if 'file' not in request.files:
            return render_template("index.html", message="No file part in the request")

        file = request.files['file']

        # Check if filename is empty
        if file.filename == '':
            return render_template("index.html", message="No selected file")

        # Check if file is allowed
        if file and allowed_file(file.filename):
            try:
                # Generate a unique, safe filename
                unique_filename = generate_unique_filename(file.filename)

                # Save the file
                file_path = os.path.join(app.config['BackupFolder'], unique_filename)
                file.save(file_path)

                return render_template("index.html", message="File successfully backed up! ✅")

            except Exception as e:
                # Log the error (in a real app, use proper logging)
                print(f"Error saving file: {e}")
                return render_template("index.html", message="An error occurred while uploading the file")

        else:
            return render_template("index.html", message="File type not allowed")

    return render_template("index.html")


@app.route('/files')
def view_files():
    """Route to display all files in the backup folder and allow downloading"""
    try:
        # List all files in the backup folder
        files = os.listdir(app.config['BackupFolder'])
        return render_template("files.html", files=files)
    except Exception as e:
        # Log the error (in a real app, use proper logging)
        print(f"Error listing files: {e}")
        return render_template("files.html", files=[])


@app.route('/download/<filename>')
def download_file(filename):
    """Serve the file for download from the backup folder"""
    try:
        # Sanitize the filename to prevent directory traversal
        safe_filename = sanitize_filename(filename)
        file_path = os.path.join(app.config['BackupFolder'], safe_filename)

        # Check if file exists
        if not os.path.exists(file_path):
            return "File not found", 404

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        # Log the error (in a real app, use proper logging)
        print(f"Error downloading file: {e}")
        return "An error occurred while downloading the file", 500


if __name__ == "__main__":
    app.run(debug=True)