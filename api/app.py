from __future__ import annotations

from flask import Flask, jsonify, request

from api.service import SimulationSessionService


def create_app() -> Flask:
    app = Flask(__name__)
    service = SimulationSessionService()

    @app.get("/api/v1/catalog")
    def catalog():
        return jsonify(service.catalog())

    @app.post("/api/v1/sessions")
    def create_session():
        payload = request.get_json(force=True) or {}
        session = service.create_session(
            disaster=payload["disaster"],
            location=payload["location"],
            population=int(payload.get("population", 1000)),
        )
        return jsonify(session.to_dict()), 201

    @app.get("/api/v1/sessions/<session_id>")
    def get_session(session_id: str):
        session = service.get_session(session_id)
        return jsonify(session.to_dict())

    @app.post("/api/v1/sessions/<session_id>/actions")
    def record_action(session_id: str):
        payload = request.get_json(force=True) or {}
        session = service.record_action(session_id, action=payload["action"])
        return jsonify(session.to_dict())

    return app
