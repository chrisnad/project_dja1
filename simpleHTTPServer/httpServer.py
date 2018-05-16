#!/usr/bin/python

import SocketServer
import SimpleHTTPServer

http_Server = SocketServer.TCPServer(("", 4444), SimpleHTTPServer.SimpleHTTPRequestHandler)
http_Server.serve_forever()