"""Tests for utils.sanitize_text"""

from pptx_to_markdown.utils import sanitize_text


class TestSanitizeText:
    # --- vertical tab (pptx line break) ---

    def test_vertical_tab_replaced_with_space_by_default(self):
        assert sanitize_text("hello\x0bworld") == "hello world"

    def test_vertical_tab_replaced_with_newline_when_specified(self):
        assert sanitize_text("hello\x0bworld", line_break="\n") == "hello\nworld"

    def test_multiple_vertical_tabs(self):
        assert sanitize_text("a\x0bb\x0bc") == "a b c"

    # --- carriage return normalisation ---

    def test_crlf_normalised_to_lf(self):
        assert sanitize_text("a\r\nb") == "a\nb"

    def test_bare_cr_normalised_to_lf(self):
        assert sanitize_text("a\rb") == "a\nb"

    # --- other control characters removed ---

    def test_null_byte_removed(self):
        assert sanitize_text("a\x00b") == "ab"

    def test_bell_removed(self):
        assert sanitize_text("a\x07b") == "ab"

    def test_form_feed_removed(self):
        assert sanitize_text("a\x0cb") == "ab"

    def test_escape_removed(self):
        assert sanitize_text("a\x1bb") == "ab"

    def test_del_removed(self):
        assert sanitize_text("a\x7fb") == "ab"

    def test_c1_control_removed(self):
        assert sanitize_text("a\x80b\x9fc") == "abc"

    # --- safe characters preserved ---

    def test_tab_preserved(self):
        assert sanitize_text("a\tb") == "a\tb"

    def test_newline_preserved(self):
        assert sanitize_text("a\nb") == "a\nb"

    def test_normal_text_unchanged(self):
        text = "Hello, World! 日本語テキスト 123"
        assert sanitize_text(text) == text

    def test_empty_string(self):
        assert sanitize_text("") == ""

    # --- combined ---

    def test_mixed_control_chars(self):
        result = sanitize_text("line1\x0bline2\x00\x1bline3")
        assert result == "line1 line2line3"

    def test_mixed_control_chars_block_mode(self):
        result = sanitize_text("line1\x0bline2\x00line3", line_break="\n")
        assert result == "line1\nline2line3"
