def test_always_passes():
    assert True

def test_flask_import():
    try:
        import flask
        assert True
    except ImportError:
        assert False
