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

        # Delete file after generation
        delete_file(filename)

    return 200


@app.route("/get_names", methods=["GET"])
def get_names():
    file_names = []
    for files in os.listdir(r"server/generated_test"):
        file_names.append(files)
    return jsonify({
        'ok': True,
        'msg': 'Success',
        'data': file_names
    })


@app.route("/download", methods=['GET'])
def send_files():
    # print("Get request called")
    # path = r"server\generated_test"
    # #return send_from_directory(directory=path, path="")
    # new_path = r"server\temp"
    file_name = ""
    # for file in os.listdir(path):
    #     file_name = file
    #     print(file_name)
    #     path += rf"\{file}"
    #     old_path = path
    #     if not os.path.exists(new_path):
    #         os.mkdir(new_path)
    #     for existing_files in os.listdir(new_path):
    #         os.remove(new_path + rf"\{existing_files}")
    #     new_path += rf"\{file}"
    #     shutil.move(old_path, new_path)
    #     break
    zip_path = r"..\Generated_files.zip"
    if os.path.exists(zip_path):
        os.remove(zip_path)
    shutil.make_archive("Generated_files", 'zip', "./generated_test")
    # print(send_path)
    return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name="Generated_tracks.zip")
    # return send_from_directory(directory=r".\generated_test", filename="")


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def model_generate_drums(input_file):
    number_steps = 128
    run_dir = r'server\drums_rnn\logdir\final_run'
    output_dir=r'server\generated_test'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

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

# Handler = CustomHTTPRequestHandler
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("serving at port", PORT)
#    httpd.serve_forever() 

# if __name__ == "__main__":
#     model_generate_drums(input_file="C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/FinalData/test/c/1_funk_80_beat_4-4_31.midi")


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
    # send_files()
    # get_names()