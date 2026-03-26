# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup (pyproject.toml, directory structure, documentation)
- `extractors/text.py`: `extract_text_frame` (bullet hierarchy), `extract_title` (plain text), `extract_notes` (speaker notes)
- `extractors/table.py`: `extract_table` converts table shapes to Markdown tables (pipe-escaped cells, newline collapsing)
- `extractors/image.py`: `extract_image` embeds pictures as base64 data URIs; `image_placeholder` for disabled-image mode
- `extractors/chart.py`: `extract_chart` converts chart series data to Markdown table with chart-type comment; handles string/numeric categories and multiple series
