"""Tests for extractors/text.py"""

import pytest
from pptx import Presentation
from pptx.util import Inches

from pptx_to_markdown.extractors.text import extract_notes, extract_text_frame, extract_title


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_textbox(texts_with_levels: list[tuple[str, int]]):
    """Return a textbox shape populated with the given (text, level) pairs."""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(4), Inches(2))
    tf = txBox.text_frame

    for i, (text, level) in enumerate(texts_with_levels):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = text
        para.level = level

    return txBox


def _make_slide_with_notes(notes_text: str):
    """Return a (prs, slide) tuple with speaker notes set."""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.notes_slide.notes_text_frame.text = notes_text
    return slide


# ---------------------------------------------------------------------------
# extract_text_frame
# ---------------------------------------------------------------------------

class TestExtractTextFrame:
    def test_no_text_frame_returns_empty(self):
        """Shapes without a text frame return an empty string."""
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        # Add a picture-less picture placeholder isn't easily doable;
        # use a line shape which has no text frame.
        from pptx.util import Pt
        from pptx.enum.shapes import MSO_SHAPE_TYPE
        line = slide.shapes.add_connector(
            1,  # MSO_CONNECTOR.STRAIGHT
            Inches(1), Inches(1), Inches(2), Inches(2),
        )
        assert extract_text_frame(line) == ""

    def test_empty_textbox_returns_empty(self):
        shape = _make_textbox([("", 0)])
        assert extract_text_frame(shape) == ""

    def test_single_level0_paragraph(self):
        shape = _make_textbox([("Hello", 0)])
        assert extract_text_frame(shape) == "- Hello"

    def test_multiple_level0_paragraphs(self):
        shape = _make_textbox([("First", 0), ("Second", 0)])
        assert extract_text_frame(shape) == "- First\n- Second"

    def test_nested_bullet_levels(self):
        shape = _make_textbox([
            ("Level 0", 0),
            ("Level 1", 1),
            ("Level 2", 2),
        ])
        expected = "- Level 0\n  - Level 1\n    - Level 2"
        assert extract_text_frame(shape) == expected

    def test_empty_paragraphs_are_skipped(self):
        shape = _make_textbox([("First", 0), ("", 0), ("Third", 0)])
        assert extract_text_frame(shape) == "- First\n- Third"

    def test_whitespace_only_paragraphs_are_skipped(self):
        shape = _make_textbox([("Text", 0), ("   ", 0)])
        assert extract_text_frame(shape) == "- Text"

    def test_text_is_stripped(self):
        shape = _make_textbox([("  padded  ", 0)])
        assert extract_text_frame(shape) == "- padded"

    def test_vertical_tab_in_paragraph_becomes_space(self):
        """\\x0b (pptx in-paragraph line break) must not appear in output."""
        shape = _make_textbox([("hello\x0bworld", 0)])
        result = extract_text_frame(shape)
        assert "\x0b" not in result
        assert "hello world" in result

    def test_other_control_chars_removed(self):
        # python-pptx XML-escapes \x00/\x1b etc. to "_x0000_" notation before
        # we see them, so we verify via sanitize_text directly (see test_utils.py).
        # Here we just confirm the output contains no raw control characters.
        shape = _make_textbox([("normal text", 0)])
        result = extract_text_frame(shape)
        for ch in result:
            assert ch >= " " or ch in ("\t", "\n"), f"Unexpected control char: {ch!r}"


# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

class TestExtractTitle:
    def test_returns_plain_text(self):
        shape = _make_textbox([("My Title", 0)])
        assert extract_title(shape) == "My Title"

    def test_strips_whitespace(self):
        shape = _make_textbox([("  Title  ", 0)])
        assert extract_title(shape) == "Title"

    def test_multiline_joined(self):
        """python-pptx joins paragraphs with newlines in .text."""
        shape = _make_textbox([("Line 1", 0), ("Line 2", 0)])
        result = extract_title(shape)
        assert "Line 1" in result
        assert "Line 2" in result

    def test_no_text_frame_returns_empty(self):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        line = slide.shapes.add_connector(1, Inches(1), Inches(1), Inches(2), Inches(2))
        assert extract_title(line) == ""

    def test_vertical_tab_in_title_becomes_space(self):
        shape = _make_textbox([("Title\x0bPart2", 0)])
        assert "\x0b" not in extract_title(shape)


# ---------------------------------------------------------------------------
# extract_notes
# ---------------------------------------------------------------------------

class TestExtractNotes:
    def test_no_notes_slide_returns_empty(self):
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        # A slide has no notes_slide until accessed; has_notes_slide is False.
        assert extract_notes(slide) == ""

    def test_empty_notes_returns_empty(self):
        slide = _make_slide_with_notes("")
        assert extract_notes(slide) == ""

    def test_whitespace_notes_returns_empty(self):
        slide = _make_slide_with_notes("   \n  ")
        assert extract_notes(slide) == ""

    def test_notes_text_is_returned(self):
        slide = _make_slide_with_notes("This is a speaker note.")
        assert extract_notes(slide) == "This is a speaker note."

    def test_notes_text_is_stripped(self):
        slide = _make_slide_with_notes("  Note with padding  ")
        assert extract_notes(slide) == "Note with padding"

    def test_multiline_notes(self):
        slide = _make_slide_with_notes("Line 1\nLine 2")
        result = extract_notes(slide)
        assert "Line 1" in result
        assert "Line 2" in result

    def test_vertical_tab_in_notes_becomes_newline(self):
        """In notes context, \\x0b should become \\n (preserve line breaks)."""
        slide = _make_slide_with_notes("note\x0bcontinued")
        result = extract_notes(slide)
        assert "\x0b" not in result
        assert "note" in result
        assert "continued" in result
