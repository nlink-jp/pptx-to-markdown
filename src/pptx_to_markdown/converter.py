"""Orchestrates per-slide conversion from Presentation to Markdown."""

from pptx import Presentation

from .extractors.chart import extract_chart
from .extractors.image import extract_image
from .extractors.table import extract_table
from .extractors.text import extract_notes, extract_text_frame


def convert(
    prs: Presentation,
    *,
    include_notes: bool = True,
    include_images: bool = True,
    include_charts: bool = True,
) -> str:
    """Convert a Presentation object to a Markdown string."""
    slides_md = []
    for i, slide in enumerate(prs.slides, start=1):
        slides_md.append(_convert_slide(slide, i, include_notes=include_notes,
                                        include_images=include_images, include_charts=include_charts))
    return "\n\n---\n\n".join(slides_md) + "\n"


def _convert_slide(
    slide,
    index: int,
    *,
    include_notes: bool,
    include_images: bool,
    include_charts: bool,
) -> str:
    """Convert a single slide to a Markdown string."""
    # TODO: implement in Phase 1-4
    raise NotImplementedError
