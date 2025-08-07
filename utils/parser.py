from datetime import datetime, timedelta
from dateutil import parser
import re


def parse_natural(text: str, lang: str) -> dict:
    """Very naive natural language parser.

    Currently supports Russian word "завтра" by converting it to the actual
    date before passing the string to :func:`dateutil.parser.parse`.

    Parameters
    ----------
    text: str
        User input describing reminder text and date/time.
    lang: str
        Currently unused, kept for future localisation.

    Returns
    -------
    dict
        Dictionary with keys ``text`` and ``date_time``.
    """

    now = datetime.now()

    # Replace the word "завтра" with tomorrow's date so that dateutil can
    # understand it. Any casing of the word is handled.
    text_to_parse = text

    if re.search(r"\bзавтра\b", text, flags=re.IGNORECASE):
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        text_to_parse = re.sub(r"\bзавтра\b", tomorrow, text_to_parse, flags=re.IGNORECASE)
    if re.search(r"\btomorrow\b", text, flags=re.IGNORECASE):
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        text_to_parse = re.sub(r"\btomorrow\b", tomorrow, text_to_parse, flags=re.IGNORECASE)

    # Convert times written with a dot to a format understood by dateutil.
    text_to_parse = re.sub(r"(\d{1,2})\.(\d{2})", r"\1:\2", text_to_parse)

    dt = parser.parse(text_to_parse, dayfirst=True, fuzzy=True)
    cleaned = re.sub(
        r"(Напомни|Remind|завтра|tomorrow|\bв\b|\bat\b|\d{1,2}[\.:]\d{2})",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    return {"text": cleaned, "date_time": dt}
