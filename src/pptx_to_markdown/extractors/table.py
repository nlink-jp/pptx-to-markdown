"""Extract table shapes from pptx to Markdown tables."""

from ..utils import sanitize_text


def _sanitize_cell(text: str) -> str:
    """Prepare cell text for Markdown: sanitize control chars, strip, escape pipes.

    Both \\x0b (pptx line break) and \\n (paragraph break) are collapsed to a
    single space so the cell stays on one line.
    """
    return sanitize_text(text, line_break=" ").replace("\n", " ").strip().replace("|", "\\|")


def extract_table(shape) -> str:
    """Convert a table shape to a Markdown table string.

    The first row is treated as the header row; a separator line is
    inserted after it. Pipe characters inside cells are escaped as \\|.
    Newlines and pptx line-break characters inside cells are collapsed to a
    single space.

    Assumes shape.has_table is True.
    Returns an empty string if the table has no rows.
    """
    table = shape.table
    if not table.rows:
        return ""

    md_rows = []
    for row in table.rows:
        cells = [_sanitize_cell(cell.text) for cell in row.cells]
        md_rows.append("| " + " | ".join(cells) + " |")

    col_count = len(table.rows[0].cells)
    separator = "| " + " | ".join(["---"] * col_count) + " |"

    return "\n".join([md_rows[0], separator] + md_rows[1:])
