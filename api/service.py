from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List
from uuid import uuid4

from Simulation.Objects import Locations
from Simulation.Simulation import Simulation


SUPPORTED_DISASTERS = [
    "asteroid",
    "earthquake",
    "hurricane",
    "invasion",
    "pandemic",
    "sun",
    "tornado",
    "wildfire",
]


@dataclass
class SessionState:
    session_id: str
    disaster: str
    location: str
    step: int
    report: str
    completed: bool
    actions_taken: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


class SimulationSessionService:
    def __init__(self) -> None:
        self._sessions: Dict[str, Simulation] = {}

    def catalog(self) -> dict:
        return {
            "disasters": SUPPORTED_DISASTERS,
            "locations": [location.name for location in Locations],
        }

    def create_session(self, disaster: str, location: str, population: int) -> SessionState:
        simulation = Simulation()
        simulation.set_disaster(disaster)
        simulation.set_location(location, {"population": population})
        session_id = str(uuid4())
        self._sessions[session_id] = simulation
        return self._snapshot(session_id, simulation)

    def get_session(self, session_id: str) -> SessionState:
        simulation = self._sessions[session_id]
        return self._snapshot(session_id, simulation)

    def record_action(self, session_id: str, action: str) -> SessionState:
        simulation = self._sessions[session_id]
        simulation.take_action(action)
        simulation.time_step()
        return self._snapshot(session_id, simulation)

    def _snapshot(self, session_id: str, simulation: Simulation) -> SessionState:
        report = ""
        if not simulation.is_complete():
            report = simulation.get_report() or ""
        return SessionState(
            session_id=session_id,
            disaster=simulation.disaster,
            location=simulation.location,
            step=simulation.current_time_step,
            report=report,
            completed=simulation.is_complete(),
            actions_taken=list(simulation.actions_taken),
        )
