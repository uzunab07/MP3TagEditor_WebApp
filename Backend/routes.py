from app import app
from flask import render_template, request, jsonify, send_from_directory, abort
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TDRC

UPLOADS_FOLDER = "uploads"
if not os.path.exists(UPLOADS_FOLDER):
    os.makedirs(UPLOADS_FOLDER)


@app.route("/")
def upload_form():
    return render_template("index.html")


@app.route("/modify")
def modify_form():
    return render_template("modify.html")


@app.route("/upload", methods=['POST'])
def upload_file():
    if 'mp3File' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['mp3File']

    file_path = os.path.join(UPLOADS_FOLDER, file.filename)
    file.save(file_path)
    
    # return render_template("index.html")

    return jsonify({"message": "File uploaded successfully"}), 200

# TODO  Processing the file


@app.route("/file_process", methods=["GET"])
def process_file():
    metadata = {
        'title': request.args.get('title'),
        'album': request.args.get('album'),
        'artist': request.args.get('artist'),
        'genre': request.args.get('genre')
    }
    # get the file name

    file_name = os.listdir(UPLOADS_FOLDER)
    # file_path = "/"+UPLOADS_FOLDER+"/"+file_name
    file_path = os.path.join(UPLOADS_FOLDER, file_name[0])

    modify_metadata(file_path, metadata)
    return render_template('modify.html', file_name=file_name), 200


# TODO downloading the file
@app.route('/download/<filename>')
def download_file(filename):
    # Security Check
    file_path = os.path.join(UPLOADS_FOLDER, filename)
    if not os.path.isfile(file_path):
        abort

    return send_from_directory(UPLOADS_FOLDER, filename, as_attachment=True)


# TODO deleting the local file


def modify_metadata(file, metadata):
    # Load the MP3 file
    audio = MP3(file, ID3=ID3)

    # Add ID3 tag if not present
    if audio.tags is None:
        audio.add_tags()

    # Modify metadata
    audio.tags.add(TIT2(encoding=3, text=metadata['title']))
    audio.tags.add(TPE1(encoding=3, text=metadata['artist']))
    audio.tags.add(TALB(encoding=3, text=metadata['album']))
    audio.tags.add(TCON(encoding=3, text=metadata['genre']))

    # Save changes
    audio.save()


def print_metadata(file_path):
    # Load the MP3 file
    audio = MP3(file_path, ID3=ID3)

    # Print general audio information
    print(f"Length: {audio.info.length} seconds")
    print(f"Bitrate: {audio.info.bitrate} bps")

    # Load ID3 tags
    id3 = audio.tags

    # Print specific metadata
    print(f"Title: {id3.get('TIT2')}")
    print(f"Artist: {id3.get('TPE1')}")
    print(f"Album: {id3.get('TALB')}")
    print(f"Genre: {id3.get('TCON')}")
    print(f"Year: {id3.get('TDRC')}")
