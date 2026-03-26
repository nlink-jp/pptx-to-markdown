"""Extract text frames and bullet hierarchies from pptx shapes."""


def extract_text_frame(shape) -> str:
    """Convert a shape's text frame to Markdown bullet list.

    Each paragraph becomes a bullet item indented by its level:
      level 0 → "- text"
      level 1 → "  - text"
      level 2 → "    - text"

    Empty paragraphs are skipped.
    Returns an empty string if the shape has no text frame or all paragraphs are empty.
    """
    if not shape.has_text_frame:
        return ""

    lines = []
    for para in shape.text_frame.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        indent = "  " * para.level
        lines.append(f"{indent}- {text}")

    return "\n".join(lines)


def extract_title(shape) -> str:
    """Return the plain text content of a title shape.

    Strips surrounding whitespace. Returns an empty string if the shape
    has no text frame.
    """
    if not shape.has_text_frame:
        return ""
    return shape.text_frame.text.strip()


def extract_notes(slide) -> str:
    """Extract speaker notes from a slide as a plain string.

    Returns an empty string if there are no notes or the notes are blank.
    """
    if not slide.has_notes_slide:
        return ""
    return slide.notes_slide.notes_text_frame.text.strip()
