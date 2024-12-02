from pathlib import Path
import shelve

import gradio as gr
import litellm
from promptic import llm


class Config:
    config_dir = Path.home() / ".demo"
    config_path = config_dir / "config.db"

    def __init__(self):
        if not self.config_dir.exists():
            print(f"Creating config directory {self.config_dir}")
            self.config_dir.mkdir(parents=True, exist_ok=True)
        # Initialize database with empty API key if it doesn't exist
        with shelve.open(str(self.config_path)) as db:
            if 'api_key' not in db:
                db['api_key'] = ''

    def get_api_key(self):
        try:
            with shelve.open(str(self.config_path)) as db:
                result = db.get('api_key', '')
                print(f"api key = {result}")
                return result
        except Exception:
            print(f"Config file {self.config_path} does not exist")
            return ""

    def set_api_key(self, api_key):
        with shelve.open(str(self.config_path)) as db:
            db['api_key'] = api_key
            litellm.api_key = api_key
            print(f"API key set to {api_key}")

config = Config()

@llm(
    memory=True,
    stream=True,
    api_key=config.get_api_key(),
)
def assistant(message):
    """{message}"""


def predict(message, history):
    partial_message = ""
    for chunk in assistant(message):
        partial_message += str(chunk)
        yield partial_message


with gr.ChatInterface(
    fn=predict,
    title="Promptic Chatbot Demo",
) as chat_interface:
    chat_interface.chatbot.clear(assistant.clear)

with gr.Blocks() as settings_interface:
    api_key = gr.Textbox(label="API Key", value=config.get_api_key())
    api_key.change(config.set_api_key, api_key)

demo = gr.TabbedInterface([chat_interface, settings_interface], ["Chat", "Settings"])

if __name__ == "__main__":
    demo.launch()
