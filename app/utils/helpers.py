"""Generic utility helpers."""


def format_confidence(value: float) -> str:
    """Convert a confidence score into a user-facing percentage string."""
    return f"{value * 100:.1f}%"
