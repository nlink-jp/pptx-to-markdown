"""CLI entry point for pptx-to-markdown."""

import sys

import click
from pptx import Presentation

from .converter import convert


@click.command()
@click.argument("input_file", type=click.Path(exists=True, readable=True, dir_okay=False))
@click.option("-o", "--output", "output_file", type=click.Path(dir_okay=False), default=None,
              help="Output file path. Defaults to stdout.")
@click.option("--no-notes", is_flag=True, default=False, help="Omit speaker notes.")
@click.option("--no-images", is_flag=True, default=False, help="Replace images with placeholders.")
@click.option("--no-charts", is_flag=True, default=False, help="Omit chart data.")
def main(input_file: str, output_file: str | None, no_notes: bool, no_images: bool, no_charts: bool) -> None:
    """Convert a .pptx file to Markdown."""
    if not input_file.lower().endswith(".pptx"):
        raise click.BadParameter("Only .pptx files are supported.", param_hint="INPUT_FILE")

    prs = Presentation(input_file)
    result = convert(prs, include_notes=not no_notes, include_images=not no_images, include_charts=not no_charts)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
    else:
        sys.stdout.write(result)
