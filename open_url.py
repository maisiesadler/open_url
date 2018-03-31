#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import webbrowser
import cgi
import check_url
import httplib

PORT_NUMBER = 8080
good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		# Send the html message
		self.wfile.write("Hello World !")
		return
	def do_POST(self):
            # Parse the form data posted
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })

            if "url" in form:
                # Begin the response
                url = form["url"].value
                status_code = check_url.get_server_status_code(url)
                if status_code in good_codes:
                    webbrowser.open(url, new=2)
                    self.send_response(200)
                else:
                    if status_code is None:
                        self.send_response(404)
                    else:
                        self.send_response(status_code)
            else:
                self.send_response(404)
                
            self.end_headers()
            return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	