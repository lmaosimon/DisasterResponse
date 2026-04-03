# Disaster Response Simulation Platform

Disaster Response is an educational crisis-management simulator that now exposes its scenario engine through a lightweight session API in addition to the original conversational interface. The project models disaster timelines, action choices, and feedback loops for training and experimentation.

## What Changed

- added a session-oriented API under [`api/`](./api)
- removed brittle path assumptions from the disaster reader
- removed an unnecessary top-level geocoding dependency from the simulation core
- replaced an unneeded `sigfig` runtime dependency with an internal helper

## Core Surfaces

- [`Simulation/`](./Simulation): disaster playback engine and location models
- [`api/app.py`](./api/app.py): Flask app for catalog and simulation-session endpoints
- [`Test/API/test_api.py`](./Test/API/test_api.py): regression tests for the new API flow
- [`www/`](./www): original Flask-based browser interface

## API Endpoints

- `GET /api/v1/catalog`
- `POST /api/v1/sessions`
- `GET /api/v1/sessions/<session_id>`
- `POST /api/v1/sessions/<session_id>/actions`

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
make test
make api
```

The API will start on `http://127.0.0.1:8000`.

## Container Workflow

```bash
make docker-build
make docker-run
```

## Verification

Run the full Python test suite:

```bash
make test
```

If you use the browser interface and want a stable Flask session secret across restarts, set:

```bash
cp .env.example .env
export DISASTER_RESPONSE_SECRET_KEY='replace-with-a-random-value'
```

## Project Direction

The repository is now structured to support multiple clients against the same simulation engine: browser UI, API consumers, and future command-line or agent integrations.
