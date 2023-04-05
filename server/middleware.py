import http.server
import socketserver
import os
from drums_rnn.drums_rnn_generate import generate_drums
from flask import Flask, render_template, request, redirect, url_for
#from drums_rnn_generate import main
#from drums_rnn_generate import run_with_flags
# import audio_processing

app = Flask(__name__)

# Change this to serve on a different port
PORT = 8080

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files["file"]
        print(type(file))
        filename = os.getcwd()
        filename = filename + "\\received_file.midi"

        # Overwrite file if it already exists
        if os.path.exists(filename):
            os.remove(filename)
        file.save(r"C:\Users\akasliwal2\Documents\FYP\Final_Year_project\received_file.midi")
        model_generate_drums(filename)
    return 'DONE'


# class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):


#     def do_POST(self):
#         filename = os.getcwd()
#         filename = filename + "/received_file.midi"

#         # Overwrite file if it already exists
#         if os.path.exists(filename):
#             with open(filename, 'wb') as file:
#                 file.write('\n'.encode('utf-8')) 
#                 file.close()
#         # Rewrite the content of the file.
#         file_length = int(self.headers['Content-Length'])
#         with open(filename, 'wb') as output_file:
#             output_file.write(self.rfile.read(file_length))
#         self.send_response(201, 'Created')
#         self.end_headers()
#         reply_body = 'Saved "%s"\n' % filename
#         self.wfile.write(reply_body.encode('utf-8'))
#         model_generate_drums(filename)
    

#     def do_GET(self):
#         pass


def model_generate_drums(input_file):
    number_steps = 128
    while not generate_drums(
        run_dir='/tmp/drums_rnn/logdir/run2',
        output_dir='/tmp/drums_rnn/generated_test',
        num_outputs=10,
        num_steps=number_steps,
        primer_midi=input_file
    ):
        number_steps += 128

# Handler = CustomHTTPRequestHandler
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("serving at port", PORT)
#    httpd.serve_forever() 

# if __name__ == "__main__":
#     model_generate_drums(input_file="C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/FinalData/test/c/1_funk_80_beat_4-4_31.midi")



if __name__ == "__main__":
    app.run(port=PORT, debug=True)
