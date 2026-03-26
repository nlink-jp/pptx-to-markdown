"""Integration tests for converter.py"""

import io

import pytest
from PIL import Image
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

from pptx_to_markdown.converter import convert


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _blank_prs() -> Presentation:
    return Presentation()


def _prs_title_only(title: str) -> Presentation:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title Slide
    slide.shapes.title.text = title
    return prs


def _prs_title_and_body(title: str, body: str, notes: str = "") -> Presentation:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
    slide.shapes.title.text = title
    slide.placeholders[1].text = body
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return prs


def _prs_with_table(title: str, rows_data: list[list[str]]) -> Presentation:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    slide.shapes.add_textbox(Inches(0), Inches(0), Inches(4), Inches(1)).text_frame.paragraphs[0].text = title

    n_rows, n_cols = len(rows_data), len(rows_data[0])
    tbl = slide.shapes.add_table(n_rows, n_cols, Inches(1), Inches(2), Inches(6), Inches(3)).table
    for r, row in enumerate(rows_data):
        for c, text in enumerate(row):
            tbl.cell(r, c).text = text
    return prs


def _prs_with_picture(title: str) -> Presentation:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    img = Image.new("RGB", (2, 2), color=(0, 255, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    slide.shapes.add_picture(buf, Inches(1), Inches(1), Inches(2), Inches(2))
    return prs


def _prs_with_chart() -> Presentation:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    chart_data = CategoryChartData()
    chart_data.categories = ["A", "B"]
    chart_data.add_series("S1", (10, 20))
    slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(1), Inches(1), Inches(6), Inches(4),
        chart_data,
    )
    return prs


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestConvert:
    def test_empty_presentation_returns_newline(self):
        result = convert(_blank_prs())
        assert result == "\n"

    def test_title_appears_in_heading(self):
        result = convert(_prs_title_only("My Slide"))
        assert "# スライド 1: My Slide" in result

    def test_slide_index_in_heading(self):
        result = convert(_prs_title_only("Hello"))
        assert "スライド 1" in result

    def test_body_text_in_output(self):
        result = convert(_prs_title_and_body("Title", "Body content"))
        assert "Body content" in result

    def test_multiple_slides_separated_by_rule(self):
        prs = Presentation()
        for i in range(3):
            slide = prs.slides.add_slide(prs.slide_layouts[0])
            slide.shapes.title.text = f"Slide {i + 1}"
        result = convert(prs)
        assert result.count("---") == 2

    def test_slide_numbers_increment(self):
        prs = Presentation()
        for i in range(2):
            slide = prs.slides.add_slide(prs.slide_layouts[0])
            slide.shapes.title.text = f"Slide {i + 1}"
        result = convert(prs)
        assert "スライド 1" in result
        assert "スライド 2" in result

    def test_notes_included_by_default(self):
        result = convert(_prs_title_and_body("T", "B", notes="Speaker note"))
        assert "Speaker note" in result
        assert "## ノート" in result

    def test_notes_excluded_when_disabled(self):
        result = convert(_prs_title_and_body("T", "B", notes="Speaker note"), include_notes=False)
        assert "Speaker note" not in result
        assert "## ノート" not in result

    def test_no_notes_section_when_notes_empty(self):
        result = convert(_prs_title_and_body("T", "B"))
        assert "## ノート" not in result

    def test_table_rendered_in_output(self):
        result = convert(_prs_with_table("T", [["A", "B"], ["1", "2"]]))
        assert "| A | B |" in result
        assert "| --- | --- |" in result

    def test_image_embedded_as_base64_by_default(self):
        result = convert(_prs_with_picture("T"))
        assert "data:image/png;base64," in result

    def test_image_replaced_by_placeholder_when_disabled(self):
        result = convert(_prs_with_picture("T"), include_images=False)
        assert "data:image/png;base64," not in result
        assert "[画像:" in result

    def test_chart_rendered_as_table_by_default(self):
        result = convert(_prs_with_chart())
        assert "<!-- チャート:" in result
        assert "| カテゴリ |" in result

    def test_chart_omitted_when_disabled(self):
        result = convert(_prs_with_chart(), include_charts=False)
        assert "<!-- チャート:" not in result

    def test_result_ends_with_newline(self):
        result = convert(_prs_title_only("T"))
        assert result.endswith("\n")
