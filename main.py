from flask import Flask, request, send_file, after_this_request, render_template, logging
from flask_cors import CORS
from utils import download_url
import os, time
app = Flask(__name__)
CORS(app)



@app.errorhandler(500)
def internal_error(error):
    app.logger.error(error)
    return "500 Server error", 500

@app.route("/", methods=["GET"])
def index():

    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.get_json().get("url")
    filename = ""
    try:
        filename = download_url(url)
    except Exception as e:
            app.logger.error(f"Error downloading file: {e}")
            return {
                "msg": f"Failed to download file from url {url}",
                "error": e,
            }, 400

    @after_this_request
    def remove_file(response):
        try:
            os.remove(filename)
        except Exception as e:
            app.logger.error(f"Error deleting file {filename}: {e}")
        return response

    return send_file(filename, as_attachment=True), 200

@app.route("/vfs/<path:file_path>", methods=["GET"])
def vfs(file_path):
    if not file_path:
        return "", 200

    


if __name__ == "__main__":
    app.run("0.0.0.0", 5500, False)
