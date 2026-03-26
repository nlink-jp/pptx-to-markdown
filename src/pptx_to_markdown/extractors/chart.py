"""Extract chart data from pptx chart shapes as Markdown tables."""


def extract_chart(shape) -> str:
    """Convert a chart shape's data to a Markdown table with a chart-type comment.

    Assumes shape.has_chart is True.

    Returns a string like:
        <!-- チャート: 棒グラフ -->
        | カテゴリ | シリーズ1 |
        |----------|-----------|
        | 項目A    | 10        |
    """
    # TODO: implement in Phase 4
    raise NotImplementedError
