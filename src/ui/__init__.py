"""UI module for NeuroForge 3D.

Re-export the `app` submodule so tests and dynamic imports can access
`src.ui.app` as an attribute of the `src.ui` package.
"""

from . import app  # re-export submodule for convenience/tests
