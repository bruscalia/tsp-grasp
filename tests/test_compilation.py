def test_compilation():
    from tspgrasp import cythonized
    assert cythonized, "Compilation failed"
