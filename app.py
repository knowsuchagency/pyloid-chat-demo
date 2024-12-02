from pyloid import Pyloid
from chatbot import demo
import threading


def run_demo():
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)


# Create and start demo thread
demo_thread = threading.Thread(target=run_demo, daemon=True)
demo_thread.start()

app = Pyloid(app_name="Pyloid-App", single_instance=True)

win = app.create_window("pyloid-example")
win.load_url("http://localhost:7860")
win.show_and_focus()

app.run()
