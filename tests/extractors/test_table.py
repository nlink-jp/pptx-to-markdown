"""Tests for extractors/table.py"""

import pytest
from pptx import Presentation
from pptx.util import Inches

from pptx_to_markdown.extractors.table import extract_table


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _make_table_shape(rows_data: list[list[str]]):
    """Return a table shape populated with rows_data[row][col] text."""
    assert rows_data, "rows_data must not be empty"
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    n_rows = len(rows_data)
    n_cols = len(rows_data[0])
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(1), Inches(1), Inches(6), Inches(3))
    for r, row in enumerate(rows_data):
        for c, text in enumerate(row):
            shape.table.cell(r, c).text = text
    return shape


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestExtractTable:
    def test_basic_two_row_table(self):
        shape = _make_table_shape([
            ["Name", "Age"],
            ["Alice", "30"],
        ])
        result = extract_table(shape)
        lines = result.splitlines()
        assert lines[0] == "| Name | Age |"
        assert lines[1] == "| --- | --- |"
        assert lines[2] == "| Alice | 30 |"

    def test_header_only_table(self):
        """Single-row table: header + separator, no data rows."""
        shape = _make_table_shape([["Col A", "Col B", "Col C"]])
        result = extract_table(shape)
        lines = result.splitlines()
        assert len(lines) == 2
        assert lines[0] == "| Col A | Col B | Col C |"
        assert lines[1] == "| --- | --- | --- |"

    def test_three_column_table(self):
        shape = _make_table_shape([
            ["A", "B", "C"],
            ["1", "2", "3"],
            ["4", "5", "6"],
        ])
        result = extract_table(shape)
        lines = result.splitlines()
        assert lines[0] == "| A | B | C |"
        assert lines[1] == "| --- | --- | --- |"
        assert lines[2] == "| 1 | 2 | 3 |"
        assert lines[3] == "| 4 | 5 | 6 |"

    def test_pipe_characters_are_escaped(self):
        shape = _make_table_shape([
            ["Key", "Value"],
            ["a|b", "c|d"],
        ])
        result = extract_table(shape)
        assert "a\\|b" in result
        assert "c\\|d" in result

    def test_newlines_in_cells_become_spaces(self):
        shape = _make_table_shape([
            ["Header"],
            ["line1\nline2"],
        ])
        result = extract_table(shape)
        assert "line1 line2" in result
        assert "\n\n" not in result.replace("|\n|", "")

    def test_cell_text_is_stripped(self):
        shape = _make_table_shape([
            ["  Header  "],
            ["  value  "],
        ])
        result = extract_table(shape)
        assert "| Header |" in result
        assert "| value |" in result

    def test_empty_cells(self):
        shape = _make_table_shape([
            ["A", ""],
            ["", "B"],
        ])
        result = extract_table(shape)
        lines = result.splitlines()
        assert lines[0] == "| A |  |"
        assert lines[2] == "|  | B |"

    def test_separator_column_count_matches_header(self):
        shape = _make_table_shape([["X", "Y", "Z", "W"]])
        result = extract_table(shape)
        separator = result.splitlines()[1]
        assert separator.count("---") == 4

    def test_vertical_tab_in_cells_becomes_space(self):
        """\\x0b (pptx in-cell line break) must not appear in output."""
        shape = _make_table_shape([
            ["Header"],
            ["cell\x0bcontent"],
        ])
        result = extract_table(shape)
        assert "\x0b" not in result
        assert "cell content" in result

    def test_other_control_chars_in_cells_removed(self):
        shape = _make_table_shape([["ok\x00val"]])
        assert "\x00" not in extract_table(shape)
