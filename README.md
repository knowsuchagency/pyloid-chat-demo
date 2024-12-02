# Pyloid Chat Demo

A desktop chat application built with Pyloid, Gradio, and Promptic, demonstrating how to create a native-feeling chatbot application with a modern UI.

## Features

- Native desktop application window
- Chat interface powered by Promptic and LLMs (Large Language Models)
- Settings panel for API key configuration
- Persistent configuration storage
- Stream-based chat responses
- Modern UI with tabbed interface

## Prerequisites

- [Python 3.12](https://www.python.org/downloads/) or higher
- [`uv` package manager](https://github.com/astral-sh/uv) (recommended)
- [`just` command runner](https://github.com/casey/just)
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Usage

1. Clone the repository:

```bash
git clone https://github.com/knowsuchagency/pyloid-chat-demo.git
```

2. Run the application:

```bash
# Build and open the application
just build open
