from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from provider import Provider
import json
# Future ssl use, leaving it here as a reminder
#import ssl

class mdgtHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
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
        return
        
    def list_providers(self):
        p = Path('providers')
        provFiles = list(p.glob('*.json'))
        provs = [pf.stem for pf in provFiles]
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(provs).encode('utf-8'))
        return
        
    def JSON_error(self, message):
        # Might want a different response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"error_message": message}).encode('utf-8'))
        return
        

def serve(port=8181):
    address = ('', port)
    httpd = HTTPServer(address, mdgtHandler)
    httpd.serve_forever()
    
 # This is just for testing
if __name__ == "__main__":
    print("Serving at http://localhost:8181")
    serve()