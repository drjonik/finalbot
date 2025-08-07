import sys
from datetime import datetime, timedelta
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.parser import parse_natural


def _expected_datetime(days_ahead: int, hour: int, minute: int) -> datetime:
    """Helper to build expected datetime objects for tests."""
    base = datetime.now() + timedelta(days=days_ahead)
    return base.replace(hour=hour, minute=minute, second=0, microsecond=0)


def test_parse_natural_russian_phrase():
    """Typical Russian reminder should extract text and tomorrow's time."""
    res = parse_natural("Напомни завтра в 10:00 купить хлеб", "ru")
    assert res["text"] == "купить хлеб"
    assert res["date_time"] == _expected_datetime(1, 10, 0)


def test_parse_natural_english_phrase():
    """English phrase with "tomorrow" should also be supported."""
    res = parse_natural("Remind tomorrow at 08:30 buy milk", "en")
    assert res["text"] == "buy milk"
    assert res["date_time"] == _expected_datetime(1, 8, 30)


def test_parse_natural_time_with_dot():
    """Times written with dots should be normalised to parse correctly."""
    res = parse_natural("Напомни завтра в 9.30 позвонить маме", "ru")
    assert res["text"] == "позвонить маме"
    assert res["date_time"] == _expected_datetime(1, 9, 30)

