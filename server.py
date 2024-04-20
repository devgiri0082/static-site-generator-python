import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


class RequestHandler(SimpleHTTPRequestHandler):
  def end_headers(self):
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Access-Control-Allow-Methods", "GET, OPTION")
    self.send_header("Access-Control-Allow-Headers", "*")
    super().end_headers()

  def do_OPTIONS(self):
    self.send_response(200, "Ok")
    self.end_headers()

def run(
  server_class = HTTPServer,
  handler_class = RequestHandler,
  port = 8080,
  address = None
):
  if address:
    os.chdir(address)
  server_address = ("", port)
  httpd = server_class(server_address, handler_class)
  print(f"Serving http on localhost:{port} from directory {address}...")
  httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Server with cors")
    parser.add_argument("--dir", help="Directory to serve from the file", default=".")
    parser.add_argument("--port", help="Port to serve HTTP on", default=8888)
    args = parser.parse_args()
    run(address= args.dir)
