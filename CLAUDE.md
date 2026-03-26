# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pptx-to-markdown` is a CLI tool that converts `.pptx` files to structured Markdown. The primary use case is preparing presentation content for LLM analysis. Images are embedded as base64 data URIs; charts are extracted as Markdown tables; speaker notes are included as a separate section.

## Development Rules

- **Security first**: validate all file inputs, never execute content from pptx files
- **Small units**: each function/class does one thing; fix issues in the smallest scope possible
- **Test alongside code**: every new extractor or converter function must have a corresponding test
- **Testable design**: pure functions preferred; side effects isolated to `cli.py`
- **Test before commit**: run the full test suite before every commit
- **Update docs on feature change**: README.md and CHANGELOG.md must be updated when features are added or changed

## Commands

```bash
# Install dependencies (including dev)
uv sync

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/extractors/test_text.py

# Run a single test by name
uv run pytest tests/extractors/test_text.py::test_extract_title

# Run with coverage
uv run pytest --cov=pptx_to_markdown

# Run the CLI
uv run pptx2md input.pptx
uv run pptx2md input.pptx -o output.md
uv run pptx2md input.pptx --no-notes --no-images
```

## Architecture

### Data Flow

```
CLI (cli.py)
  └─ Converter (converter.py)          # orchestrates per-slide conversion
       ├─ extractors/text.py           # title, body text, bullet hierarchy
       ├─ extractors/table.py          # Shape tables → Markdown tables
       ├─ extractors/image.py          # pictures → base64 data URIs
       └─ extractors/chart.py          # chart series data → Markdown tables
```

### Key Design Points

- **Extractors are pure functions**: each `extract_*` function takes a `python-pptx` shape object and returns a string (Markdown fragment). No I/O, no global state.
- **Converter assembles slides**: `converter.py` iterates slides, calls the appropriate extractor per shape type, and joins the fragments into a full Markdown document.
- **CLI handles I/O**: `cli.py` owns file reading/writing and option parsing. It passes a `Presentation` object to the converter, not a file path.
- **Shape type dispatch**: shape types are identified via `shape.shape_type` and `shape.has_text_frame` / `shape.has_table` / `shape.has_chart`. The converter dispatches to the correct extractor.

### Output Format

Each slide renders as:

```markdown
# スライド N: タイトル

本文・箇条書き

| col | col |
|-----|-----|
| ... | ... |

<!-- チャート: チャート種別 -->
| ... |

![説明](data:image/png;base64,...)

## ノート

発表者ノート

---
```

## Package Structure

```
src/pptx_to_markdown/
  cli.py          # click CLI, file I/O only
  converter.py    # Presentation → full Markdown string
  extractors/
    text.py       # text frames and bullet hierarchy
    table.py      # table shapes
    image.py      # picture shapes → base64
    chart.py      # chart shapes → data table
tests/
  fixtures/       # sample .pptx files for integration tests
  extractors/     # unit tests per extractor
  test_converter.py
  conftest.py     # shared fixtures (load sample pptx)
```
