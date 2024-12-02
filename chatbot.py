import gradio as gr
from promptic import llm

from config import Config

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
