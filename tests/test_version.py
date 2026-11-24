"""The version the package reports matches the one it is installed as."""

from importlib.metadata import version

from pptx_to_markdown import __version__


def test_version_matches_package_metadata() -> None:
    assert __version__ == version("pptx-to-markdown")
