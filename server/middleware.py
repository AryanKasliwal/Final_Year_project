import http.server
import socketserver
import os
import shutil
from drums_rnn.drums_rnn_generate import generate_drums
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory, send_file
import sched, time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Change this to serve on a different port
PORT = 8080

music_generated = False
generation_dir = r"server/generated_test"
zip_dir = "./Generated_files"
rnn_checkpoint_dir = r'server/drums_rnn/logdir/final_run'

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        print(type(file))
        filename = r".\received_file.midi"

        # Overwrite file if it already exists, then save received file
        delete_file(filename)
        file.save(filename)

        # Generate drums from the received file
        model_generate_drums(filename)

        # Delete received file after generation
        delete_file(filename)

    return 200


@app.route("/get_names", methods=["GET"])
def get_names():
    file_names = []
    for files in os.listdir(generation_dir):
        file_names.append(files)
    return jsonify({
        'ok': True,
        'msg': 'Success',
        'data': file_names
    })


@app.route("/download", methods=['GET'])
def send_files():
    zip_path = r".\Generated_files.zip"
    delete_file(zip_path)
    shutil.make_archive(zip_dir, 'zip', generation_dir)
    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name="Generated_tracks.zip")


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def model_generate_drums(input_file):
    number_steps = 128
    run_dir = rnn_checkpoint_dir
    output_dir=generation_dir

    delete_directory(output_dir)

    # number_steps decides the length of the track.
    # Start with a low value and keep increasing it until 
    # the length of generated part of track is greater than the input track
    while not generate_drums(
        run_dir=run_dir,
        output_dir=output_dir,
        num_outputs=10,
        num_steps=number_steps,
        primer_midi=input_file
    ):
        number_steps += 128
    global music_generated
    music_generated = True


if __name__ == "__main__":
    app.run(port=PORT, debug=True)