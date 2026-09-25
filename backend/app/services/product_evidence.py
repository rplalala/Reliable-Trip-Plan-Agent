"""In-memory normalized presentation context; never changes research output or trace files."""

from backend.app.evidence.experience_models import ExperienceProfile
from backend.app.evidence.models import WeatherEvidence


class ProductEvidenceCollector:
    def __init__(self, tracer):
        self.tracer = tracer
        self.weather: WeatherEvidence | None = None
        self.summaries: dict[str, str] = {}
        self.deadline: float | None = None

    def __getattr__(self, name):
        return getattr(self.tracer, name)

    def event(self, name, payload=None):
        if name == "application_request_deadline":
            self.deadline = payload["deadline"]
        self.tracer.event(name, payload)

    def payload(self, category, name, value, *, minimum_mode):
        if category == "evidence":
            if name == "weather_evidence" and isinstance(value, WeatherEvidence):
                self.weather = value
            elif name == "v1_experience_profile" and isinstance(value, ExperienceProfile):
                if value.summary:
                    self.summaries[value.place_id] = value.summary
        self.tracer.payload(category, name, value, minimum_mode=minimum_mode)
