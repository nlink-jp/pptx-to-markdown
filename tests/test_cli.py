"""Tests for the CLI (cli.py)."""

import pytest
from click.testing import CliRunner
from pptx import Presentation

from pptx_to_markdown.cli import main


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _save_simple_pptx(path, title: str = "Test") -> None:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    prs.save(str(path))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestCLI:
    def test_stdout_output(self, tmp_path):
        pptx = tmp_path / "deck.pptx"
        _save_simple_pptx(pptx, "Hello")
        result = CliRunner().invoke(main, [str(pptx)])
        assert result.exit_code == 0
        assert "Hello" in result.output

    def test_file_output(self, tmp_path):
        pptx = tmp_path / "deck.pptx"
        out = tmp_path / "out.md"
        _save_simple_pptx(pptx, "FileOut")
        result = CliRunner().invoke(main, [str(pptx), "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        assert "FileOut" in out.read_text(encoding="utf-8")

    def test_rejects_non_pptx_extension(self, tmp_path):
        txt = tmp_path / "deck.txt"
        txt.write_bytes(b"not a pptx")
        result = CliRunner().invoke(main, [str(txt)])
        assert result.exit_code != 0

    def test_no_notes_flag(self, tmp_path):
        pptx = tmp_path / "deck.pptx"
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        slide.shapes.title.text = "T"
        slide.notes_slide.notes_text_frame.text = "Secret note"
        prs.save(str(pptx))

        result = CliRunner().invoke(main, [str(pptx), "--no-notes"])
        assert result.exit_code == 0
        assert "Secret note" not in result.output

    def test_no_images_flag(self, tmp_path):
        import io
        from PIL import Image
        from pptx.util import Inches

        pptx = tmp_path / "deck.pptx"
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        img = Image.new("RGB", (2, 2), color=(255, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        slide.shapes.add_picture(buf, Inches(1), Inches(1), Inches(2), Inches(2))
        prs.save(str(pptx))

        result = CliRunner().invoke(main, [str(pptx), "--no-images"])
        assert result.exit_code == 0
        assert "data:image/png;base64," not in result.output
        assert "[画像:" in result.output

    def test_no_charts_flag(self, tmp_path):
        from pptx.chart.data import CategoryChartData
        from pptx.enum.chart import XL_CHART_TYPE
        from pptx.util import Inches

        pptx = tmp_path / "deck.pptx"
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        chart_data = CategoryChartData()
        chart_data.categories = ["X"]
        chart_data.add_series("S", (1,))
        slide.shapes.add_chart(
            XL_CHART_TYPE.COLUMN_CLUSTERED,
            Inches(1), Inches(1), Inches(5), Inches(3),
            chart_data,
        )
        prs.save(str(pptx))

        result = CliRunner().invoke(main, [str(pptx), "--no-charts"])
        assert result.exit_code == 0
        assert "<!-- チャート:" not in result.output
