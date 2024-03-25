import os
import http.server
import utils

# Serve the HTML content directly from Markdown
class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that includes logger support.

    This class extends the SimpleHTTPRequestHandler provided by the http.server module
    to include logging functionality.

    Attributes:
        markdown_file (st): The markdown file
        logger (Logger): A logger instance for logging messages.
    """
    
    def __init__(self, request, client_address, server, markdown_file, logger):
        """
        Initialize the HTTPHandler.

        Args:
            request (socket): The request socket.
            client_address (tuple): A tuple containing the client's address (IP, port).
            server (HTTPServer): The HTTP server instance.
            markdown_file (str): The markdown file
            logger (Logger): A logger instance for logging messages.
        """
        self.markdown_file = markdown_file
        self.logger = logger
        super().__init__(request, client_address, server)

    def log_message(self, format, *args):
        """
        Log a message.

        Args:
            format: The format string for the log message.
            *args: Arguments to be formatted into the log message.
        """
        self.logger.info("%s - %s" % (self.address_string(), format % args))

    def do_GET(self):
        """
        Handle GET requests.

        If the requested path ends with 'pygments.css', serve the CSS file.
        If the requested path ends with '.md', convert Markdown to HTML and serve.
        Otherwise, serve files as usual.
        """
        # Strip leading and trailing slashes from the path
        path = self.path.strip("/")

        # Check if the requested path is for pygments.css
        if path.endswith("pygments.css"):
            self._serve_css_file(path)
        elif path.endswith(".md"):
            self.logger.debug("trying to open %s", path)
            self._serve_markdown_file(path)
        else:
            self.send_error(404, "File not found")


    def _serve_css_file(self, path):
        """
        Serve the pygments.css file.
        """
        # Construct the absolute path to pygments.css based on the location of server.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(script_dir, "pygments.css")

        # Serve the content of pygments.css
        try:
            with open(css_path, 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def _serve_markdown_file(self, path):
        """
        Serve the Markdown file as HTML.
        """
        markdown_file_name = os.path.basename(self.markdown_file)

        self.logger.debug("markdown name: %s", markdown_file_name)
        self.logger.debug("request markdown path: %s", path)

        if markdown_file_name.lower() != path.lower():
            self.logger.debug("Trying to get file different that using in the app: %s - %s", markdown_file_name, path)
            self.send_response(404, "File not found")
            self.end_headers()
            return

        self.logger.debug("markdown file path: %s", self.markdown_file)
        if not os.path.exists(self.markdown_file):
            self.send_response(404, "File not found")
            self.end_headers()
            return
        with open(self.markdown_file, 'r') as file:
            markdown_content = file.read()
            html_content = utils.convert_to_html(markdown_content)
            html_content_with_websocket = f"""<!DOCTYPE html>
<html>
<head>
    <title>{path}</title>
    <meta charset="UTF-8">
    <style>
        body {{
            color: rgb(36, 36, 36);
            font-family: source-serif-pro, Georgia, Cambria, "Times New Roman", Times, serif;
            font-size: 20px;
            word-break: break-word;
        }}

        h1, h2, h3 {{
            color: rgb(36, 36, 36);        
            font-family: sohne, "Helvetica Neue", Helvetica, Arial, sans-serif;
        }}

        h1 {{
            font-size: 42px;
            font-weight: 700;
            margin-top: 49.98px;
            margin-bottom: 20px;
            line-height:52px;
        }}

        h2 {{
            font-size: 24px;
            font-weight: 600;
            margin-top: 46.8px;
            margin-bottom: 20px;
            line-height: 30px;
        }}

        h3 {{
            font-size: 18px;
            font-weight: 510;
            margin-top: 43.5px;
            margin-bottom: 20px;
            line-height: 24px;
        }}

        img {{
            max-width: 100%;
        }}

        a {{
            color: inherit;
        }}

        blockquote {{
            border-left: 2px solid black;
            padding-left: 10px;
            font-style: italic;
        }}

        body :not(pre) >  code {{
            background-color: rgb(242, 242, 242);
            color: rgb(36, 36, 36);
            font-family: source-code-pro, Menlo, Monaco, "Courier New", Courier, monospace;
            font-size: 15px;
            padding: 2px 4px;
        }}

        .header {{
            align-items: center;
            border-bottom: solid 1px #f2f2f2;
            display: flex;
            height: 57px;
        }}

        .header span {{
            font-family: "Mona Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 24px;
            font-weight: 600;
        }}

        .container {{
            display: flex;
            justify-content: center;
        }}

        .content {{
            max-width: 680px;
            width: 680px;
        }}

    </style>
    <link href="pygments.css" rel="stylesheet">
    <script>
        var ws = new WebSocket("ws://localhost:8765");
        ws.onmessage = function(event) {{
            document.body.getElementsByClassName('content')[0].innerHTML = event.data; 
        }};
    </script>
</head>
<body><div class="header"><span>miaul</span></div><div class="container"><div class="content">{html_content}</div></div></body>
</html>"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content_with_websocket.encode())

