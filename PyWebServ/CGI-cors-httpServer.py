import os
import sys
import urllib
import BaseHTTPServer
import SimpleHTTPServer
import select
import copy
import CGIHTTPServer

class CORSRequestHandler (CGIHTTPServer.CGIHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        CGIHTTPServer.CGIHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)