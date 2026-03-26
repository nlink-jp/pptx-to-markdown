"""Extract chart data from pptx chart shapes as Markdown tables."""

from pptx.oxml.ns import qn

from ..utils import sanitize_text


def _get_series_categories(series) -> list[str]:
    """Return the category labels for a series by reading its XML.

    Handles both string categories (c:strCache) and numeric categories
    (c:numCache). Returns an empty list if no category data is found.
    """
    cat_elem = series._element.find(qn("c:cat"))
    if cat_elem is None:
        return []

    for cache_tag in (qn("c:strCache"), qn("c:numCache")):
        cache = cat_elem.find(f".//{cache_tag}")
        if cache is not None:
            return [
                sanitize_text(pt.find(qn("c:v")).text or "", line_break=" ")
                for pt in cache.findall(qn("c:pt"))
                if pt.find(qn("c:v")) is not None
            ]

    return []


def _format_value(v) -> str:
    """Format a series value as a string; represent None as empty."""
    if v is None:
        return ""
    # Drop unnecessary trailing zeros for floats that are whole numbers
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def extract_chart(shape) -> str:
    """Convert a chart shape's data to a Markdown table with a chart-type comment.

    Output format:
        <!-- チャート: CHART_TYPE_NAME -->
        | カテゴリ | シリーズ1 | シリーズ2 |
        |----------|-----------|-----------|
        | 項目A    | 10        | 20        |

    When no series are present only the comment line is returned.
    Assumes shape.has_chart is True.
    """
    chart = shape.chart
    chart_type_name = chart.chart_type.name if chart.chart_type else "不明"
    comment = f"<!-- チャート: {chart_type_name} -->"

    series_list = list(chart.series)
    if not series_list:
        return comment

    categories = _get_series_categories(series_list[0])
    series_names = [
        sanitize_text(s.name or f"シリーズ{i + 1}", line_break=" ")
        for i, s in enumerate(series_list)
    ]

    header_cells = (["カテゴリ"] if categories else []) + series_names
    header = "| " + " | ".join(header_cells) + " |"
    separator = "| " + " | ".join(["---"] * len(header_cells)) + " |"

    all_values = [list(s.values) for s in series_list]
    n_points = max(len(v) for v in all_values) if all_values else 0

    rows = []
    for i in range(n_points):
        cells = []
        if categories:
            cells.append(categories[i] if i < len(categories) else "")
        for vals in all_values:
            cells.append(_format_value(vals[i] if i < len(vals) else None))
        rows.append("| " + " | ".join(cells) + " |")

    return "\n".join([comment, header, separator] + rows)
