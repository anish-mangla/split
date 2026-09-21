# Split

Backend for the Split application.

## Setup

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -e .

## Run

Start the API server:

    uvicorn backend.server:app --reload

The API runs at:

    http://127.0.0.1:8000