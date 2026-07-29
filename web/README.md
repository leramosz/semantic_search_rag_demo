# Semantic Search & RAG UI

This project is a static frontend demo for a semantic search and RAG-style chat interface.

It is designed to run locally with Python's built-in HTTP server and connect to a backend API endpoint for chat queries.

## Features

- Clean single-page chat UI.
- Suggested prompts for quick testing.
- Sends user queries to a configurable backend endpoint.
- Renders assistant responses in chat format.

## How it works

```text
Browser -> Static HTML/CSS/JS -> Backend API (/ask)
```

The frontend is fully static and does not require a build step.

## Requirements

- Python 3.11+.
- A backend API running separately.
- A browser.

## Run locally

From the folder that contains `index.html`, start a simple static server:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```

## Configuration

The UI sends requests to the endpoint configured in the input field on the left side of the page.

Default value:

```text
http://127.0.0.1:8000/ask
```

If your backend runs on a different host or port, update that field before sending messages.

## Backend contract

The frontend expects a JSON request like:

```json
{
  "query": "your question",
  "top_k": 5
}
```

And it expects a response containing an `answer` field.

Example:

```json
{
  "answer": "Here is the answer..."
}
```

## Notes

- The page is static, so `python3 -m http.server 8080` is enough to serve it.
- The backend must allow CORS if it is on a different origin.
- The theme is automatically initialized from the user's system preference.
- Suggested prompts are included to help test the UI quickly.

## Troubleshooting

### The page loads but the chat does not answer
Check that the backend API is running and that the endpoint is correct.

### I get a CORS error
Make sure the backend allows requests from the frontend origin.

### I see a 404 when opening the page
Verify that `index.html` is in the same folder where you run the server.

## Goal of the demo

This UI was built to present a semantic search and RAG experience in a clean, simple, and portfolio-friendly way.