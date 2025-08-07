"""Utility helpers for converting user text into structured reminders."""

from dataclasses import dataclass
from datetime import datetime
import re
from dateutil import parser


@dataclass
class ParsedTask:
    """Simple container for data extracted from a natural language request."""

    text: str
    date_time: datetime
    repeat: str | None = None


def parse_natural(text: str, lang: str) -> ParsedTask:
    """Parse a natural language reminder description.

    The original implementation returned a plain ``dict``. Downstream callers
    expected attributes like ``parsed.text`` and ``parsed.date_time`` which
    caused an ``AttributeError`` at runtime.  Returning a dataclass makes the
    structure explicit and avoids such errors.

    Args:
        text: Raw user message containing the reminder request.
        lang: Language code (currently unused but kept for future NLP).

    Returns:
        ParsedTask: Structured representation of the reminder.
    """

    # ``fuzzy=True`` allows the parser to ignore unknown words such as
    # "Напомни" or "завтра" while still extracting a valid datetime.
    dt = parser.parse(text, dayfirst=True, fuzzy=True)

    cleaned = re.sub(
        r"(Напомни|Remind|завтра|в|\d{1,2}[\.:]\d{2})",
        "",
        text,
    ).strip()
    return ParsedTask(text=cleaned, date_time=dt)
