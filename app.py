from pyloid import Pyloid
from chatbot import demo
import threading
import time
import socket
from contextlib import contextmanager

HOST = "127.0.0.1"
PORT = 7861


def run_demo():
    demo.launch(
        server_name=HOST,
        server_port=PORT,
        share=False,
        show_api=False,
    )


# Create and start demo thread
demo_thread = threading.Thread(target=run_demo, daemon=True)
demo_thread.start()

app = Pyloid(app_name="Pyloid-App", single_instance=True)

win = app.create_window("pyloid-example")


@contextmanager
def wait_for_server(host=HOST, port=PORT, timeout=30):
    start_time = time.time()
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex((host, port)) == 0:
                    break
        except:
            pass

        if time.time() - start_time > timeout:
            raise TimeoutError(
                f"Server at {host}:{port} did not start within {timeout} seconds"
            )

        time.sleep(0.5)

    yield


with wait_for_server():
    win.load_url(f"http://{HOST}:{PORT}")
    win.show_and_focus()

app.run()
