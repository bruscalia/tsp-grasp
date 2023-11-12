from tspgrasp.cython.utils import python_cmin, python_cmax, python_carg_min, python_carg_max, python_cpop
from tspgrasp.cython.constructive import python_range_idx


def test_cmin():
    x = [5, 9, 3, 2, 7]
    out = python_cmin(x)
    assert out == 2.0, f"Failed to identify cmin {out}"


def test_cmax():
    x = [5, 9, 3, 2, 7]
    out = python_cmax(x)
    assert out == 9.0, f"Failed to identify cmax {out}"


def test_carg_min():
    x = [5, 9, 3, 2, 7]
    out = python_carg_min(x)
    assert out == 3, f"Failed to identify carg min {out}"


def test_cmax():
    x = [5, 9, 3, 2, 7]
    out = python_carg_max(x)
    assert out == 1, f"Failed to identify carg max {out}"


def test_cpop_good():
    x = [5, 9, 3, 2, 7]
    v, out = python_cpop(x, 2)
    assert out == 3, f"Failed to pop correct element {out}"
    assert v == [5, 9, 2, 7], f"Failed to modify inplace {v}, {x}"


def test_cpop_above():
    x = [5, 9, 3, 2, 7]
    v, out = python_cpop(x, 10)
    assert out == 7, f"Failed to pop correct element (above) {out}"
    assert v == [5, 9, 3, 2], f"Failed to modify inplace (above) {v}, {x}"


def test_range_idx():
    x = [5, 9, 3, 2, 7]
    out = python_range_idx(x)
    assert out == list(range(len(x))), f"Failed to produce range of index {out}"
