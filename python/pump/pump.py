#!/usr/bin/python3

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from state import State

import RPi.GPIO as GPIO
import random
import sys
import json

class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""
    state = State()

    def log_message(self, format, *args):
        pass

    def handleCommand(self, cmd):
        # cmd: 'Toggle' / 'Off' / 'On'
        # valve: [1-8]
        # pump: 'All'
        print(cmd)
        try:
            match cmd["cmd"].lower():
                case 'toggle':
                    state = 2
                case 'off':
                    state = 0
                case 'on':
                    state = 1
                case _:
                    raise Exception("Command not accepted")
            if "valve" in cmd:
                valve = cmd["valve"]
                if valve<1 or valve>8:
                    raise Exception("Valve index out of range")
            elif "pump" in cmd:
                valve = 0
            else:
                raise Exception("Object missing (valve or pump")
            self.state.setValue(valve, state)
            return True, "Ok"
        except:
            print("{}".format(sys.exc_info()[0]))
            return False, "Check server logs"

    def do_GET(self):
        try:
            #print("GET Request for " + self.path + " from " + self.client_address[0])
            if self.path in ["/favicon.ico","/pump.html","/garden.png"]:
                file_to_open = open("." + self.path, 'rb').read()
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(file_to_open)
                return
            elif self.path in ["/pump-status"]:
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                res = {
                #   "valves": "{:08b}".format(random.randint(0,255)),
                #   "pump": "{:01b}".format(random.randint(0,1)),
                  "valves": self.state.getValves(),
                  "pump": self.state.getPump(),
                  "status": self.state.getStatus()
                }                
                self.wfile.write(json.dumps(res).encode())
                return
            else:
                self.send_response(HTTPStatus.TEMPORARY_REDIRECT)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Location', '/pump.html')
                self.end_headers()
                return

        except:
            print("{}".format(sys.exc_info()[0]))
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Check server logs")

    def do_POST(self):
        try:
            #print("POST Request for " + self.path);
            if self.path in ["/pump-command"]:
                content_length = int(self.headers['Content-Length'])
                post_data_json = self.rfile.read(content_length)
                post_data = json.loads(post_data_json)
                result, output = self.handleCommand(post_data)
                if result:
                    self.send_response(HTTPStatus.ACCEPTED)
                else:
                    self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(output.encode())
            else:
                self.send_response(HTTPStatus.FORBIDDEN)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                return
        except:
            print("{}".format(sys.exc_info()[0]))
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, "Check server logs")


#class StoppableHTTPServer(HTTPServer):
class StoppableHTTPServer(ThreadingHTTPServer):
    def run(self):
        restart = True
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            restart = False
            pass
        finally:
            self.server_close()
            return restart

def main():
    port = 8000
    server = StoppableHTTPServer(('', port), webserverHandler)
    # ctx = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    # ctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    # server.socket = ctx.wrap_socket(server.socket, server_side=True)
    print("Web server running on port %s" % port)
    while server.run():
        print("Web server restarted")
        sleep(1)
    GPIO.cleanup()
    

if __name__ == '__main__':
    main()

