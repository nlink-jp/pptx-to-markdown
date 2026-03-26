"""Extract picture shapes from pptx as base64 data URIs."""

import base64


def extract_image(shape, slide_index: int, image_index: int) -> str:
    """Convert a picture shape to a Markdown image tag with base64 data URI.

    Args:
        shape: A pptx shape whose .image attribute holds the picture data.
        slide_index: 1-based slide number (used in alt text).
        image_index: 1-based image counter within the slide (used in alt text).

    Returns:
        Markdown image syntax: ![スライドN_画像M](data:<mime>;base64,<data>)
    """
    b64 = base64.b64encode(shape.image.blob).decode("ascii")
    content_type = shape.image.content_type
    alt = f"スライド{slide_index}_画像{image_index}"
    return f"![{alt}](data:{content_type};base64,{b64})"


def image_placeholder(slide_index: int, image_index: int) -> str:
    """Return a placeholder string for when image output is disabled."""
    return f"[画像: スライド{slide_index}_画像{image_index}]"
