"""Tests that lock down V0 prompt behavior."""

from backend.app.versions.v0.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT


def test_itinerary_prompt_requires_exact_datetime_components() -> None:
    prompt = " ".join(ITINERARY_GENERATION_SYSTEM_PROMPT.split())

    assert "always provide all three datetime components" in prompt
    assert "date must use exactly YYYY-MM-DD" in prompt
    assert "time must use exactly HH:MM:SS" in prompt
    assert "including seconds when they are 00" in prompt
    assert "utc_offset must use exactly +HH:MM or -HH:MM" in prompt
    assert "date 2026-10-01, time 13:30:00, utc_offset +09:00" in prompt
    assert "Do not abbreviate 13:30:00 to 13:30" in prompt
