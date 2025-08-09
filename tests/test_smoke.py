def test_imports():
    import importlib

    assert importlib.import_module("interactive_portfolio") is not None
