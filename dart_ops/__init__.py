# dart_ops package
# Agent code lives at project root (agent.py, registry.py, db_helper.py, tools.py)
# This package provides the FastAPI app and utilities for deployment.
try:
    from . import agent
except (ImportError, ValueError):
    import agent
