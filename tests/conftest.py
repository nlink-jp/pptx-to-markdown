"""Shared pytest fixtures."""

import pytest
from pptx import Presentation


@pytest.fixture
def empty_presentation():
    """Return a blank Presentation with no slides."""
    return Presentation()
