"""Tests for extractors/image.py"""

import base64
import io

import pytest
from PIL import Image
from pptx import Presentation
from pptx.util import Inches

from pptx_to_markdown.extractors.image import extract_image, image_placeholder


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_png_bytes(width: int = 2, height: int = 2) -> bytes:
    """Create a minimal valid PNG image and return its bytes."""
    img = Image.new("RGB", (width, height), color=(255, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def _make_picture_shape(image_bytes: bytes):
    """Add a picture shape to a blank slide and return the shape."""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    buf = io.BytesIO(image_bytes)
    return slide.shapes.add_picture(buf, Inches(1), Inches(1), Inches(2), Inches(2))


# ---------------------------------------------------------------------------
# extract_image
# ---------------------------------------------------------------------------

class TestExtractImage:
    def test_returns_markdown_image_syntax(self):
        shape = _make_picture_shape(_make_png_bytes())
        result = extract_image(shape, slide_index=1, image_index=1)
        assert result.startswith("![")
        assert "](data:" in result
        assert ";base64," in result

    def test_alt_text_contains_slide_and_image_index(self):
        shape = _make_picture_shape(_make_png_bytes())
        result = extract_image(shape, slide_index=3, image_index=2)
        assert "スライド3_画像2" in result

    def test_content_type_in_data_uri(self):
        shape = _make_picture_shape(_make_png_bytes())
        result = extract_image(shape, slide_index=1, image_index=1)
        assert "data:image/png;base64," in result

    def test_base64_decodes_to_original_blob(self):
        """The embedded base64 must round-trip back to the original image bytes."""
        png_bytes = _make_png_bytes()
        shape = _make_picture_shape(png_bytes)
        result = extract_image(shape, slide_index=1, image_index=1)

        # Extract base64 payload from the data URI
        b64_part = result.split(";base64,")[1].rstrip(")")
        decoded = base64.b64decode(b64_part)
        assert decoded == shape.image.blob

    def test_different_indices_produce_different_alt_text(self):
        png_bytes = _make_png_bytes()
        shape1 = _make_picture_shape(png_bytes)
        shape2 = _make_picture_shape(png_bytes)
        r1 = extract_image(shape1, slide_index=1, image_index=1)
        r2 = extract_image(shape2, slide_index=1, image_index=2)
        assert r1 != r2
        assert "画像1" in r1
        assert "画像2" in r2

    def test_slide_index_reflected_in_alt_text(self):
        shape = _make_picture_shape(_make_png_bytes())
        r = extract_image(shape, slide_index=5, image_index=1)
        assert "スライド5" in r


# ---------------------------------------------------------------------------
# image_placeholder
# ---------------------------------------------------------------------------

class TestImagePlaceholder:
    def test_placeholder_format(self):
        assert image_placeholder(1, 1) == "[画像: スライド1_画像1]"

    def test_indices_reflected(self):
        assert image_placeholder(3, 2) == "[画像: スライド3_画像2]"

    def test_different_indices_produce_different_placeholders(self):
        assert image_placeholder(1, 1) != image_placeholder(1, 2)
        assert image_placeholder(1, 1) != image_placeholder(2, 1)
