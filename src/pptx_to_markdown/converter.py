"""Orchestrates per-slide conversion from Presentation to Markdown."""

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER

from .extractors.chart import extract_chart
from .extractors.image import extract_image, image_placeholder
from .extractors.table import extract_table
from .extractors.text import extract_notes, extract_text_frame, extract_title


def convert(
    prs: Presentation,
    *,
    include_notes: bool = True,
    include_images: bool = True,
    include_charts: bool = True,
) -> str:
    """Convert a Presentation object to a Markdown string.

    Slides are joined by a horizontal rule (---). Returns a trailing newline.
    """
    slides_md = [
        _convert_slide(
            slide, i,
            include_notes=include_notes,
            include_images=include_images,
            include_charts=include_charts,
        )
        for i, slide in enumerate(prs.slides, start=1)
    ]
    return "\n\n---\n\n".join(slides_md) + "\n"


def _is_title_placeholder(shape) -> bool:
    """Return True if the shape is a title or center-title placeholder."""
    if not shape.is_placeholder:
        return False
    ph_type = shape.placeholder_format.type
    return ph_type in (PP_PLACEHOLDER.TITLE, PP_PLACEHOLDER.CENTER_TITLE)


def _convert_slide(
    slide,
    index: int,
    *,
    include_notes: bool,
    include_images: bool,
    include_charts: bool,
) -> str:
    """Convert a single slide to a Markdown string."""
    parts = []

    # --- heading ---
    title = ""
    for shape in slide.shapes:
        if _is_title_placeholder(shape):
            title = extract_title(shape)
            break
    parts.append(f"# スライド {index}: {title}" if title else f"# スライド {index}")

    # --- body shapes ---
    image_count = 0
    for shape in slide.shapes:
        if _is_title_placeholder(shape):
            continue

        if shape.has_chart:
            if include_charts:
                parts.append(extract_chart(shape))
        elif shape.has_table:
            parts.append(extract_table(shape))
        elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            image_count += 1
            if include_images:
                parts.append(extract_image(shape, index, image_count))
            else:
                parts.append(image_placeholder(index, image_count))
        elif shape.has_text_frame:
            text = extract_text_frame(shape)
            if text:
                parts.append(text)

    # --- speaker notes ---
    if include_notes:
        notes = extract_notes(slide)
        if notes:
            parts.append(f"## ノート\n\n{notes}")

    return "\n\n".join(parts)
