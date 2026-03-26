"""Tests for extractors/chart.py"""

import pytest
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

from pptx_to_markdown.extractors.chart import extract_chart


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_chart_shape(chart_type, categories: list[str], series_data: list[tuple[str, tuple]]):
    """Return a chart shape with the given categories and series."""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    chart_data = CategoryChartData()
    chart_data.categories = categories
    for name, values in series_data:
        chart_data.add_series(name, values)

    return slide.shapes.add_chart(
        chart_type,
        Inches(1), Inches(1), Inches(6), Inches(4),
        chart_data,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestExtractChart:
    def test_comment_line_present(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["A", "B"],
            [("S1", (1, 2))],
        )
        result = extract_chart(shape)
        assert result.startswith("<!-- チャート:")
        assert "-->" in result.splitlines()[0]

    def test_chart_type_name_in_comment(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["A"],
            [("S1", (1,))],
        )
        result = extract_chart(shape)
        assert "COLUMN_CLUSTERED" in result.splitlines()[0]

    def test_header_row_with_category_column(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.BAR_CLUSTERED,
            ["X", "Y"],
            [("Sales", (10, 20))],
        )
        lines = extract_chart(shape).splitlines()
        assert lines[1] == "| カテゴリ | Sales |"

    def test_separator_row(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["A"],
            [("S1", (5,)), ("S2", (6,))],
        )
        lines = extract_chart(shape).splitlines()
        # comment, header, separator, data...
        assert lines[2] == "| --- | --- | --- |"

    def test_data_rows_values(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["Jan", "Feb"],
            [("Revenue", (100, 200))],
        )
        lines = extract_chart(shape).splitlines()
        assert lines[3] == "| Jan | 100 |"
        assert lines[4] == "| Feb | 200 |"

    def test_categories_appear_in_first_column(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.LINE,
            ["Q1", "Q2", "Q3"],
            [("Profit", (10, 20, 30))],
        )
        result = extract_chart(shape)
        assert "Q1" in result
        assert "Q2" in result
        assert "Q3" in result

    def test_multiple_series(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["A", "B"],
            [("Alpha", (1, 2)), ("Beta", (3, 4))],
        )
        lines = extract_chart(shape).splitlines()
        assert lines[1] == "| カテゴリ | Alpha | Beta |"
        assert lines[3] == "| A | 1 | 3 |"
        assert lines[4] == "| B | 2 | 4 |"

    def test_whole_number_floats_have_no_decimal(self):
        """Values like 10.0 should render as '10', not '10.0'."""
        shape = _make_chart_shape(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            ["X"],
            [("S1", (10.0,))],
        )
        result = extract_chart(shape)
        assert "10.0" not in result
        assert "| 10 |" in result

    def test_line_chart_type_name(self):
        shape = _make_chart_shape(
            XL_CHART_TYPE.LINE,
            ["A"],
            [("S1", (1,))],
        )
        result = extract_chart(shape)
        assert "LINE" in result.splitlines()[0]
