import os
import shutil
from drums_rnn.drums_rnn_generate import generate_drums as rnn_generate_drums
from jukebox.sample import run as vqvae_generate_drums
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

PORT = 8080

music_generated = False

# Default locations used throughout the server
generation_dir = r"server/generated_test"
zip_dir = "./Generated_files"
rnn_checkpoint_dir = r'server/drums_rnn/logdir/final_run'
fName = ""
fExtension = ""


# Receives the uploaded file from client and feeds it into their chosen model
@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        model = request.form["model"]
        global fName
        global fExtension
        received_name = request.form["filename"].split(".")
        fName = received_name[0]
        fExtension = received_name[1]

        print(fName)
        filename = r".\received_file.midi"

        # Overwrite file if it already exists, then save received file
        delete_file(filename)
        file.save(filename)

        # Generate drums from the received file
        if model == "RNN":
            rnn_model_generate_drums(filename)
        else:
            rnn_model_generate_drums(filename)
            # vqvae_model_generate_drums(filename)

        # Delete received file after generation
        delete_file(filename)

    return 200

# Sends back the names of generated files
@app.route("/get_names", methods=["GET"])
def get_names():
    file_names = []
    global fName
    global fExtension
    name_counter = 1
    for files in os.listdir(generation_dir):
        os.rename(generation_dir + "/" + files, generation_dir + (f"/{fName}_{name_counter}.{fExtension}"))
        name_counter += 1
    for files in os.listdir(generation_dir):
        file_names.append(files)
    return jsonify({
        'ok': True,
        'msg': 'Success',
        'data': file_names
    })


@app.route("/download", methods=['GET'])
def send_files():
    zip_path = r"..\Generated_files.zip"
    delete_file(zip_path)
    shutil.make_archive(zip_dir, 'zip', generation_dir)
    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name="Generated_tracks.zip")


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def rnn_model_generate_drums(input_file):
    number_steps = 128
    run_dir = rnn_checkpoint_dir
    output_dir=generation_dir

    delete_directory(output_dir)

    # number_steps decides the length of the track.
    # Start with a low value and keep increasing it until 
    # the length of generated part of track is greater than the input track
    while not rnn_generate_drums(
        run_dir=run_dir,
        output_dir=output_dir,
        num_outputs=10,
        num_steps=number_steps,
        primer_midi=input_file
    ):
        number_steps += 128
    global music_generated
    music_generated = True


def vqvae_model_generate_drums(input_file):
    model = "5b"
    name = "sample_5b_prompted"
    levels = 3
    mode = "primed"
    audio_file = input_file
    prompt_length_in_seconds = 12
    sample_length_in_seconds = 20
    total_sample_length_in_seconds = 180
    sr = 44100
    n_samples = 6
    hop_fraction = 0.5, 0.5, 0.125

    vqvae_generate_drums(
        model=model, 
        mode=mode, 
        audio_file=audio_file, 
        prompt_length_in_seconds=prompt_length_in_seconds,
        name=name,
        levels=levels,
        sample_length_in_seconds=sample_length_in_seconds,
        total_sample_length_in_seconds=total_sample_length_in_seconds,
        sr=sr,
        n_samples=n_samples,
        hop_fraction=hop_fraction
    )


if __name__ == "__main__":
    app.run(port=PORT, debug=True)