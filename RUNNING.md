# Provenance Guard — Running the Capstone

## Environment

- Python: 3.13.18
- Supported Python versions: 3.11, 3.12, 3.13
- Application: Flask
- AI model: GPT-2 (`gpt2`)
- Model token limit: 400
- Maximum submission length: 10,000 characters
- Execution: Local CPU-compatible deployment
- Logging: JSON Lines

## Installation

From a clean checkout of the repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt

```

## Starting the Service

Activate the virtual environment, then start the service:

```bash
gunicorn --bind 127.0.0.1:5000 --workers 1 --timeout 180 app:app
```

The service runs locally at http://127.0.0.1:5000.

## Model Requirements

- Model: GPT-2 (`gpt2`)
- Maximum model tokens: 400
- Approximate initial download: 550 MB
- Model files are downloaded to the Hugging Face cache, not stored in this repository.
- The initial download requires internet access.
- The first inference may be slower due to initialization.

## Structured Logging

The application writes JSON Lines records to:

`logs/audit.jsonl`

Operational records include:
- UTC timestamp
- Creator identifier
- Input character count
- HTTP status
- Execution duration in milliseconds
- Completion or rejection status

Full submitted text is not stored in operational records.

## Smoke Test

With the server running, open another terminal and execute:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"creator_id":"smoke_test","text":"This is a valid sample paragraph for testing the Provenance Guard classification service."}'
```

A successful request should return HTTP 200 and a classification result.

## Preliminary Performance

Development-machine observations:

- Initial request: 73.64 seconds
- Subsequent requests: 0.09, 0.06, 0.06 seconds
- Average subsequent request: 0.07 seconds

These are preliminary observations, not the final capstone measurements.

## Known Limitations

- Deployment is local only.
- First-time model download requires internet access.
- Performance depends on available hardware.
- Rate limiting uses in-memory storage.
- Classification is not definitive proof of authorship.
