"""Extract text frames and bullet hierarchies from pptx shapes."""

from pptx.util import Pt


def extract_text_frame(shape) -> str:
    """Convert a shape's text frame to Markdown (title or body with bullet hierarchy).

    Returns an empty string if the shape has no text frame.
    """
    # TODO: implement in Phase 1
    raise NotImplementedError


def extract_notes(slide) -> str:
    """Extract speaker notes from a slide as a plain string.

    Returns an empty string if there are no notes.
    """
    # TODO: implement in Phase 1
    raise NotImplementedError
