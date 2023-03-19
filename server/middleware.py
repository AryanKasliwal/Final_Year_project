import http.server
import socketserver
import os
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

Handler = CustomHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever() 