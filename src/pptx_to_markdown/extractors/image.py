"""Extract picture shapes from pptx as base64 data URIs."""


def extract_image(shape, slide_index: int, image_index: int) -> str:
    """Convert a picture shape to a Markdown image tag with base64 data URI.

    Args:
        shape: A pptx shape with shape_type == MSO_SHAPE_TYPE.PICTURE.
        slide_index: 1-based slide number (used in alt text).
        image_index: 1-based image counter within the slide (used in alt text).

    Returns:
        Markdown image syntax: ![alt](data:image/png;base64,...)
    """
    # TODO: implement in Phase 3
    raise NotImplementedError


def image_placeholder(slide_index: int, image_index: int) -> str:
    """Return a placeholder string for when images are disabled."""
    return f"[画像: スライド{slide_index}_画像{image_index}]"
