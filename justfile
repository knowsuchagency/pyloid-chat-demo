pyloid:
    uv run app.py

format:
    uvx ruff format *.py

build:
    uv run pyinstaller app.spec --noconfirm

open:
    open dist/app

reset-config:
    rm -rf .config/pyloid_demo
