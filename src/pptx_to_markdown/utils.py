"""Shared text utilities."""

import re

# Matches control characters that should be removed:
# - C0 controls excluding HT (\x09), LF (\x0a), VT (\x0b), CR (\x0d)
#   (VT and CR are handled separately before this regex runs)
# - DEL (\x7f)
# - C1 controls (\x80-\x9f)
_REMOVE_RE = re.compile(r"[\x00-\x08\x0c\x0e-\x1f\x7f\x80-\x9f]")


def sanitize_text(text: str, *, line_break: str = " ") -> str:
    """Remove or replace non-printable control characters from *text*.

    Processing order:
    1. Normalize ``\\r\\n`` and bare ``\\r`` to ``\\n``.
    2. Replace ``\\x0b`` (vertical tab / pptx in-paragraph line break) with
       *line_break* (default ``" "`` for inline contexts such as bullets and
       table cells; pass ``"\\n"`` for block contexts such as speaker notes).
    3. Strip remaining C0/C1 control characters (everything except ``\\t``
       and ``\\n``).

    Normal printable text and whitespace (space, tab, newline) pass through
    unchanged.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\x0b", line_break)
    return _REMOVE_RE.sub("", text)
