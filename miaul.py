import asyncio
import websockets
import socketserver
import threading
import http.server
import socketserver
import os
import time
import logging
import utils
import argparse
from websocket_server import WebSocketServer  
from http_handler import HTTPHandler


# ASCII art representation of a cat
cat_ascii = """
  /\_/\\
 ( o.o )
  > ^ <
"""

# Constants
CHECK_INTERVAL_SECONDS = 1
DEFULT_BINDING_PORT = "0.0.0.0"

async def generate_and_send_html(socket_server: WebSocketServer, markdown_file: str) -> None:
    last_modified_time = os.path.getmtime(markdown_file)
    try:
        while True:
            modified_time = os.path.getmtime(markdown_file)
            if modified_time != last_modified_time:
                logger.info("%s updated", markdown_file)
                last_modified_time = modified_time
                with open(markdown_file, 'r') as file:
                    markdown_content = file.read()
                    html_content = utils.convert_to_html(markdown_content)
                    await socket_server.dispatch(html_content)
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
    except FileNotFoundError:
        print(f"Markdown file '{markdown_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def serve_http(port: int, markdown_file: str, logger) -> None:
    """
    Start an HTTP server.

    Args:
        markdown_file (str): The markdown file
        logger: Logger instance for logging messages.
        port (int): The port number to serve HTTP requests on.
    """
    with http.server.ThreadingHTTPServer((DEFULT_BINDING_PORT, port), lambda *args, **kwargs: HTTPHandler(*args, markdown_file=markdown_file, logger=logger, **kwargs)) as httpd:
        logger.info('HTTP server serving at port %s', port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nHTTP server stopped by user.")
            httpd.server_close()

if __name__ == "__main__":
    # Print start
    print('miaul is running...')
    print(cat_ascii)

    # Argument parsing
    parser = argparse.ArgumentParser(description="Miaul: Markdown In-browser Automatic Loader")
    parser.add_argument("markdown_file", help="Path to the Markdown file")
    parser.add_argument("-v", "--verbose", action="count", default=1, help="Increase output verbosity")
    args = parser.parse_args()

    # Configure logging verbosity
    log_level = logging.ERROR if args.verbose == 0 else logging.INFO if args.verbose == 1 else logging.DEBUG
    logging.basicConfig(level=log_level, format='miaul: %(asctime)s - %(levelname)s - %(module)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    markdown_file = args.markdown_file

    # Start http server
    start_http_server = threading.Thread(target=serve_http, args=(8000, markdown_file, logger,))
    start_http_server.daemon = True
    start_http_server.start()

    # Start socket server
    socket_server = WebSocketServer()
    websocket_server = websockets.serve(socket_server.echo, DEFULT_BINDING_PORT, 8765)

    # Start the WebSocket server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(websocket_server)

    asyncio.ensure_future(generate_and_send_html(socket_server, markdown_file))


    # Keep the event loop running
    loop.run_forever()
