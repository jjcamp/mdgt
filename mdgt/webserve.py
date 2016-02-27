'''webserve.py
mdgt web server module.
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from provider import Provider
import json
# Future ssl use, leaving it here as a reminder
# import ssl


class mdgtHandler(BaseHTTPRequestHandler):
    '''HTTP Request Handler
    Extends BaseHTTPRequestHandler in order to process HTTP GET requests.
    '''
    def do_GET(self):
        '''Processes HTTP GET requests'''
        args = self.path.split('/', 3)
        if len(args) < 2:
            self.JSON_error("Not enough parameters.")
        elif args[1] == "providers":
            self.list_providers()
        elif len(args) == 3:
            try:
                prov = Provider(args[1])
            except:
                self.JSON_error("Provider does not exist. " + args[1])
                return
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(prov.scrape(args[2])).encode('utf-8'))
        else:
            self.JSON_error("Invalid arguments.")

    def list_providers(self):
        '''Outputs a list of providers.'''
        p = Path('providers')
        provFiles = list(p.glob('*.json'))
        provs = [pf.stem for pf in provFiles]
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(provs).encode('utf-8'))

    def JSON_error(self, message):
        '''Outputs an error message.

        Args:
            message (str): A useful error message.
        '''
        # Might want a different response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error_message": message}).encode('utf-8'))


def serve(port=8181):
    '''Starts a web server service.

    Args:
        port (Optional[int]): The port the server should listen at.  Defaults
            to 8181.
    '''
    address = ('', port)
    httpd = HTTPServer(address, mdgtHandler)
    try:
        print("Starting web server at http://localhost:{0!s}".format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping web server.")
        httpd.socket.close()
