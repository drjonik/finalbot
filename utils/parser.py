from dataclasses import dataclass
from datetime import datetime
import re

from dateutil import parser


@dataclass
class ParsedTask:
    """Simple container for parsed task data."""

    text: str
    date_time: datetime
    repeat: str | None = None


def parse_natural(text: str, lang: str) -> ParsedTask:
    """Parse a natural language reminder into structured data."""

    dt = parser.parse(text, dayfirst=True)
    cleaned = re.sub(r"(Напомни|Remind|завтра|в|\d{1,2}[\.:]\d{2})", "", text).strip()
    return ParsedTask(text=cleaned, date_time=dt)
