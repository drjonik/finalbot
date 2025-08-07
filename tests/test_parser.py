import datetime
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from utils.parser import parse_natural, ParsedTask


def test_parse_natural_returns_parsed_task():
    text = "Напомни в 10:00 почитать книгу"
    parsed = parse_natural(text, 'ru')
    assert isinstance(parsed, ParsedTask)
    assert parsed.text == "почитать книгу"
    assert isinstance(parsed.date_time, datetime.datetime)
    assert parsed.date_time.hour == 10
    assert parsed.repeat is None
