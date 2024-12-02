# Building a Desktop Chat Application in Python with Minimal Code

Let's build a desktop chat application that streams responses from an LLM. We'll use three key libraries that work beautifully together:

- **[Pyloid](https://github.com/pyloid/pyloid)**: Creates native desktop applications -- like Electron but with Python
- **[Gradio](https://gradio.app)**: Builds the chat interface
- **[Promptic](https://github.com/knowsuchagency/promptic)**: Handles LLM interactions



https://github.com/user-attachments/assets/74b2834b-3702-4b31-8a43-79ada47ecf01



## Prerequisites

Before running the application, you'll need:
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- [uv](https://github.com/astral-sh/uv) for Python package management
- [just](https://github.com/casey/just) command runner

## The Chat Interface

First, let's create the chat interface. This is where Gradio and Promptic work together:

```python
import gradio as gr
from promptic import llm

@llm(memory=True, stream=True)
def assistant(message):
    """{message}"""

def predict(message, history):
    partial_message = ""
    for chunk in assistant(message):
        partial_message += str(chunk)
        yield partial_message

with gr.ChatInterface(
    fn=predict,
    title="Chat Demo",
) as chat_interface:
    chat_interface.chatbot.clear(assistant.clear)
```

The code above:
- Uses Promptic's `@llm` decorator to handle LLM interactions
- Implements streaming responses using a generator
- Creates a chat interface with Gradio
- By passing `memory=True`, `promptic` will manage conversation history

## Making It a Desktop App

Now, let's wrap our chat interface in a native window using Pyloid:

```python
from pyloid import Pyloid
import threading
import time
import socket
from contextlib import contextmanager

HOST = "127.0.0.1"
PORT = 7861

def run_demo():
    chat_interface.launch(
        server_name=HOST,
        server_port=PORT,
        share=False,
        show_api=False,
    )

# Run Gradio in a separate thread
demo_thread = threading.Thread(target=run_demo, daemon=True)
demo_thread.start()

app = Pyloid(app_name="Chat-App", single_instance=True)
win = app.create_window("chat-window")

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
            raise TimeoutError(f"Server at {host}:{port} did not start within {timeout} seconds")
        time.sleep(0.5)
    yield

with wait_for_server():
    win.load_url(f"http://{HOST}:{PORT}")
    win.show_and_focus()

app.run()
```

This code:
- Runs the Gradio interface in a background thread
- Creates a native window that loads the interface
- Ensures the server is ready before loading the UI

## Running the Application

This project includes a [`justfile`](https://just.systems/man/en/) with commands for building and running the application. It also uses [`uv`](https://github.com/astral-sh/uv) for package management.

```bash
# clone the repo
git clone https://github.com/knowsuchagency/pyloid-chat-demo
cd pyloid-chat-demo

# this builds the application and opens it
# it will create a virtual environment and
# install the dependencies automatically
just build open
```

That's it! With just these few lines of code, you have a desktop chat application with streaming responses. The magic comes from combining these libraries:

- Promptic handles the LLM interaction and streaming
- Gradio provides the chat interface
- Pyloid wraps everything in a native window

You can now extend this foundation by adding features like API key configuration, custom themes, or system prompts.
