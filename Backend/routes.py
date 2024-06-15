from app import app
from flask import render_template, request, jsonify
import os

@app.route("/")
def upload_form():
    return render_template("index.html")

@app.route("/upload",methods=['POST'])
def upload_file():
     file = request.files['mp3File']
     file_path = os.path.join('uploads', file.filename)
     file.save(file_path)
     
     return jsonify({"message": "File uploaded successfully"}), 200

# TODO  Processing the file


# TODO downloading the file

# TODO deleting the file
