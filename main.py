from flask import Flask, request, send_file, after_this_request, render_template, jsonify
from flask_cors import CORS
from utils import download_url
from vfs import *
from werkzeug.utils import secure_filename
import os, time, logging, tempfile

# --- Flask app setup ---
app = Flask(__name__)
CORS(app)

# --- Logging configuration ---
logging.basicConfig(filename="server.log",
                    level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def log_error(error):
    app.logger.error(error)

# --- Error handling ---
@app.errorhandler(500)
def internal_error(error):
    log_error(error)
    return "500 Server error", 500

# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.get_json().get("url")
    app.logger.debug(f"Downloading from url -> {url}")
    try:
        # Save to a unique temporary file
        filename = tempfile.mktemp()
        filename = download_url(url, filename=filename)
    except Exception as e:
        log_error(f"Error downloading file: {e}")
        return jsonify({
            "msg": f"Failed to download file from url {url}",
            "error": str(e),
        }), 400

    @after_this_request
    def cleanup_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            log_error(f"Error deleting file {filename}: {e}")
        return response

    return send_file(filename, as_attachment=True), 200

@app.route("/vfs/<path:file_path>", methods=["GET"])
def vfs_route(file_path):
    return render_template("index.html", file_path=file_path)

@app.route("/get-file", methods=["POST"])
def get_file():
    path = request.get_json().get("path")
    try:
        paths = vfs_get_path(path)
    except Exception as e:
        log_error(e)
        return jsonify({"msg": str(e)}), 400

    return jsonify({"paths": paths}), 200

@app.route("/add-file", methods=["POST"])
def add_file():
    directory = request.get_json().get("directory")
    if "file" not in request.files:
        return jsonify({"msg": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"msg": "No selected file"}), 400

    safe_filename = secure_filename(file.filename)
    filepath = os.path.join(directory, safe_filename)
    try:
        file.save(vfs_safe_path(filepath))
    except Exception as e:
        log_error(e)
        return jsonify({"msg": str(e)}), 400

    return jsonify({"msg": f"File uploaded successfully: {filepath}"}), 200

@app.route("/remove-file", methods=["POST"])
def remove_vfs_file():
    path = request.get_json().get("path")
    if not path:
        return jsonify({"msg": "No path provided"}), 400

    try:
        vfs_remove_path(path)
    except Exception as e:
        log_error(e)
        return jsonify({"msg": str(e)}), 400

    return jsonify({"msg": f"Successfully removed path: {path}"}), 200

@app.route("/icon/<path:type>", methods=["GET"])
def icon(type):
    icon_path = os.path.join("static", "icons", f"{type}.png")
    if not os.path.exists(icon_path):
        return jsonify({"msg": f"Icon {type} not found"}), 404
    return send_file(icon_path), 200

@app.route("/logs", methods=["GET"])
def logs():
    return render_template("log.html")

@app.route("/get-log", methods=["GET"])
def get_log():
    if not os.path.exists("server.log"):
        return jsonify([]), 200
    with open("server.log", "r") as file:
        return jsonify(file.readlines()), 200

# --- Run server ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=False)
