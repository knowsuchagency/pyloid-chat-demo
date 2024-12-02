from pathlib import Path
import shelve

import gradio as gr
import litellm
from promptic import llm


class Config:
    config_dir = Path.home() / ".demo"
    config_path = config_dir / "config.db"
    key = "api_key"

    def __init__(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with shelve.open(str(self.config_path)) as db:
            db.setdefault(self.key, '')

    def get_api_key(self):
        try:
            with shelve.open(str(self.config_path)) as db:
                result = db.get(self.key, '')
                litellm.api_key = result
                return result
        except Exception:
            return ""

    def set_api_key(self, value):
        with shelve.open(str(self.config_path)) as db:
            db[self.key] = value
            litellm.api_key = value


config = Config()

@llm(
    memory=True,
    stream=True,
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
