# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Control characters (especially `\x0b` / pptx in-paragraph line break) in extracted text now sanitized:
  - `\x0b` → space in bullet text, titles, and table cells
  - `\x0b` → newline in speaker notes (preserves line structure)
  - Other C0/C1 control characters (NUL, ESC, DEL, etc.) are stripped

## [0.1.0] - 2026-03-26

### Added
- Initial project setup (pyproject.toml, uv, hatchling, directory structure)
- `extractors/text.py`: `extract_text_frame` (bullet hierarchy with level-based indentation), `extract_title` (plain text), `extract_notes` (speaker notes)
- `extractors/table.py`: `extract_table` — converts table shapes to Markdown tables with pipe-escaped cells and newline collapsing
- `extractors/image.py`: `extract_image` — embeds pictures as base64 data URIs; `image_placeholder` for disabled-image mode
- `extractors/chart.py`: `extract_chart` — extracts chart series data (string/numeric categories, multiple series) as a Markdown table with chart-type comment
- `converter.py`: `convert` — orchestrates full Presentation→Markdown conversion with per-shape-type dispatch
- `cli.py`: `pptx2md` CLI with `-o`, `--no-notes`, `--no-images`, `--no-charts` flags
- MIT license (© magifd2)
- English README and Japanese README (README.ja.md)
- 65 unit and integration tests

[Unreleased]: https://github.com/magifd2/pptx-to-markdown/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/magifd2/pptx-to-markdown/releases/tag/v0.1.0
