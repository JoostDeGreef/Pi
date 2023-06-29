#!/usr/bin/python3

from http import HTTPStatus

from http.server import BaseHTTPRequestHandler, HTTPServer

import cgi
import sys

class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""

    def do_GET(self):
        try:
            print("Request for " + self.path);
            if self.path in ["/favicon.ico","/pump.html"]:
                file_to_open = open("." + self.path, 'rb').read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(file_to_open)
                return
            elif self.path in ["/pump-status"]:
                self.send_response(200)
                self.end_headers()
                self.wfile.write("01101100".encode())
                return
            else:
                self.send_response(HTTPStatus.TEMPORARY_REDIRECT)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Location', '/pump.html')
                self.end_headers()
                return

        except IOError:
            self.send_error(404, "File not found.")

    def do_POST(self):
        try:
            self.send_response(HTTPStatus.MOVED_PERMANENTLY) # weird!
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type'))
            content_len = int(self.headers.get('Content-length'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                message_content = fields.get('message')
            output = ''
            output += '<html><body>'
            output += '<h2> Okay, How about this: </h2>'
            output += '<h1> %s </h1>' % message_content[0]
            output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2> What would you like me to say?</h2><input name="message" type="text" /><input type="submit" value="Submit" /></form>'
            output += '</body></html>'
            self.wfile.write(output.encode())
            print(output)
        except:
            self.send_error(404, "{}".format(sys.exc_info()[0]))
            print(sys.exc_info())


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        # ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
        # ctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
        # server.socket = ctx.wrap_socket(server.socket, server_side=True)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print(" ^C entered stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()

