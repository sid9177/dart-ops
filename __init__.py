try:
    from . import agent
except (ImportError, ValueError):
    import agent
