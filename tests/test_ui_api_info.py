"""Tests for Gradio API info sanitization.

This ensures that `Blocks.get_api_info()` can be called and that
the returned structure does not contain plain boolean nodes in places
where a JSON Schema object is expected. Plain booleans are allowed as
values of the `const` key (JSON Schema standard), but should not
appear as a schema node itself.
"""

def test_get_api_info_sanitized():
    from src.ui.app import NeuroForgeApp

    app = NeuroForgeApp()
    blocks = app.create_interface()

    # Should not raise
    info = blocks.get_api_info()
    assert isinstance(info, dict)
    assert "named_endpoints" in info or "unnamed_endpoints" in info

    # Walk the tree; fail if any dict has a value that is a bare bool
    # except when the dict key is exactly 'const' (allowed in JSON Schema).
    def check(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, bool) and k != "const":
                    raise AssertionError(f"Found bare bool at {path + '.' + k if path else k}")
                check(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                check(v, f"{path}[{i}]")

    check(info)
