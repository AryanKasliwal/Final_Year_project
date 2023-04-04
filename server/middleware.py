import http.server
import socketserver
import os
#from drums_rnn_generate import main
#from drums_rnn_generate import run_with_flags
# import audio_processing

# Change this to serve on a different port
PORT = 8080

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):


    def do_POST(self):
        filename = os.getcwd()
        filename = filename + "/received_file.midi"

        # Overwrite file if it already exists
        if os.path.exists(filename):
            with open(filename, 'wb') as file:
                file.write('\n')
                file.close()
        # Rewrite the content of the file.
        file_length = int(self.headers['Content-Length'])
        with open(filename, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, 'Created')
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode('utf-8'))
        generate_drums(filename)


def generate_drums(input_file):
    os.system(f'cmd /k "drums_rnn_generate --config=drum_kit --run_dir=/tmp/drums_rnn/logdir/run2 --hparams="batch_size=64,rnn_layer_sizes=[256, 256]" --output_dir=/tmp/drums_rnn/generated_test --num_outputs=10 --num_steps=512 --primer_midi={input_file}"')

#Handler = CustomHTTPRequestHandler
#with socketserver.TCPServer(("", PORT), Handler) as httpd:
#    print("serving at port", PORT)
#    httpd.serve_forever() 

if __name__ == "__main__":
    generate_drums(input_file="C:/Users/akasliwal2/Documents/FYP/Final_Year_project/Dataset/FinalData/test/c/1_funk_80_beat_4-4_31.midi")