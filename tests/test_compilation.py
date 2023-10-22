def test_compilation():
    from tspgrasp.utils import cythonized
    assert cythonized, "Compilation failed"
