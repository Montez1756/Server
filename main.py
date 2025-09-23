from flask import Flask, request, send_file, after_this_request, render_template, logging, jsonify
from flask_cors import CORS
from utils import download_url
from vfs import *
import os, time
app = Flask(__name__)
CORS(app)

def log_error(error):
    app.logger.error(error)

@app.errorhandler(500)
def internal_error(error):
    log_error(error)
    return "500 Server error", 500

@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.get_json().get("url")
    app.logger.debug(f"Downloading from url -> {url}")
    filename = ""
    try:
        filename = download_url(url)
    except Exception as e:
            log_error(f"Error downloading file: {e}")
            return {
                "msg": f"Failed to download file from url {url}",
                "error": e,
            }, 400

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            log_error(f"Error deleting file {filename}: {e}")
        return response

    return send_file(filename, as_attachment=True), 200

@app.route("/vfs/<path:file_path>", methods=["GET"])
def vfs(file_path):
    return render_template("index.html", file_path=file_path)
@app.route("/get-file", methods=["POST"])
def get_file():
    path = request.get_json().get("path")

    try:
        paths = vfs_get_path(path)
    except Exception as e:
        log_error(e)
        return jsonify({"msg":str(e)}), 400

    return 
@app.route("/add-file", methods=["POST"])
def add_file():
    directory = request.get_json().get("directory")
    if  "file" not in request.files:
        return jsonify({"msg":"No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"msg": "No selected file"}), 400

    filepath = os.path.join(directory, file.filename)
    try:
        file.save(vfs_safe_path(filepath))
    except Exception as e:
        log_error(e)
        return jsonify({"msg":str(e)}), 400

    return jsonify({"msg":f"File uploaded successfully: {filepath}"}), 200
@app.route("/remove-file", methods=["POST"])
def remove_file():
    path = request.get_json().get("path")

    if path:
        try:
            vfs_remove_path(path)
        except Exception as e:
            log_error(e)
            return jsonify({"msg":str(e)}), 400
        return jsonify({"msg":f"Successfully removed path: {path}"}), 200
if __name__ == "__main__":
    app.run("0.0.0.0", 5500, False)
