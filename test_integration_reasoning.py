"""
Integration-style tests for reasoning fallback.

These tests start tiny HTTP servers (in threads) to emulate Open Web UI
and Ollama endpoints and verify that the reasoning engine will try
Open Web UI and fall back to Ollama when OW fails.
"""
import threading
import http.server
import socketserver
import json
import time
import unittest
from urllib.parse import urlparse

import reasoning_engine


class SimpleHandler(http.server.BaseHTTPRequestHandler):
    response_text = ''
    response_json = None
    status = 200

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        # respond with configured body
        self.send_response(self.status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if self.response_json is not None:
            self.wfile.write(json.dumps(self.response_json).encode())
        else:
            self.wfile.write(self.response_text.encode())

    def log_message(self, format, *args):
        # silence
        return


def start_server(handler_cls):
    # Start server on an ephemeral port and return (httpd, port)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler_cls)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, port


class TestIntegrationReasoning(unittest.TestCase):
    def setUp(self):
        # choose ephemeral ports
        self.ow_port = 18080
        self.ollama_port = 18081

    def test_ow_success(self):
        # OW returns json -> engine uses it
        class OWHandler(SimpleHandler):
            response_json = {'response': 'ow-ok'}

        httpd, port = start_server(OWHandler)
        try:
            reasoning_engine.CFG.update({
                'open_webui_endpoint': f'http://127.0.0.1:{port}/api',
                'ollama_endpoint': f'http://127.0.0.1:{self.ollama_port}/api',
                'use_open_webui': True,
                'open_webui_retries': 1,
            })
            out = reasoning_engine.query_ollama('hi', use_open_webui=True)
            self.assertIn('ow-ok', out)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_ow_fail_fallback(self):
        # OW server that returns error; Ollama returns success
        class OWHandler(SimpleHandler):
            status = 500

        class OllamaHandler(SimpleHandler):
            response_json = {'response': 'ollama-ok'}

        httpd1, port1 = start_server(OWHandler)
        httpd2, port2 = start_server(OllamaHandler)
        try:
            reasoning_engine.CFG.update({
                'open_webui_endpoint': f'http://127.0.0.1:{port1}/api',
                'ollama_endpoint': f'http://127.0.0.1:{port2}/api',
                'use_open_webui': True,
                'open_webui_retries': 1,
                'open_webui_retry_delay': 0.0,
            })

            out = reasoning_engine.query_ollama('test', use_open_webui=True)
            self.assertIn('ollama-ok', out)
        finally:
            httpd1.shutdown()
            httpd1.server_close()
            httpd2.shutdown()
            httpd2.server_close()


if __name__ == '__main__':
    unittest.main()
