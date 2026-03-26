# pptx-to-markdown

A CLI tool that converts `.pptx` files to structured Markdown. Designed as a preprocessing step for LLM-based analysis of presentation and internal documents.

[日本語版 README はこちら](README.ja.md)

## Features

- Converts slide text and bullet hierarchies to Markdown
- Renders tables as Markdown tables
- Embeds images as base64 data URIs
- Extracts chart data as Markdown tables
- Outputs speaker notes as a separate section per slide

## Requirements

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/magifd2/pptx-to-markdown.git
cd pptx-to-markdown
uv sync
```

## Usage

```bash
# Output to stdout
uv run pptx2md input.pptx

# Output to file
uv run pptx2md input.pptx -o output.md

# Omit images (replaced with placeholders)
uv run pptx2md input.pptx --no-images

# Omit speaker notes
uv run pptx2md input.pptx --no-notes

# Omit chart data
uv run pptx2md input.pptx --no-charts
```

## Output Format

```markdown
# スライド 1: Slide Title

- Bullet point
  - Nested bullet

| Col A | Col B |
| --- | --- |
| val 1 | val 2 |

<!-- チャート: COLUMN_CLUSTERED -->
| カテゴリ | Series1 |
| --- | --- |
| Item A | 10 |

![スライド1_画像1](data:image/png;base64,...)

## ノート

Speaker notes text

---

# スライド 2: Next Slide
```

Chart type names follow python-pptx's `XL_CHART_TYPE` enum (e.g. `COLUMN_CLUSTERED`, `BAR_CLUSTERED`, `LINE`, `PIE`).

## Development

```bash
# Install dependencies (including dev)
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=pptx_to_markdown
```

## Limitations

- `.ppt` (legacy format) is not supported
- Animation and transition data are not converted
- Shapes inside group shapes are not processed

## License

MIT © magifd2
