import pytest

from merchantsguide.roman2int import roman2int


def test_invalid_inputs():
    with pytest.raises(ValueError):
        roman2int("ILLEGAL")

    with pytest.raises(ValueError):
        roman2int("MIMI")

    with pytest.raises(ValueError):
        roman2int("IIII")

    with pytest.raises(ValueError):
        roman2int("IXI")

    with pytest.raises(ValueError):
        roman2int("I I")


def test_valid_inputs():
    with open('./roman_test_input', 'r') as f:
        lines = f.readlines()

    for l in lines:
        i, o = l.strip().split(" ")
        assert roman2int(i) == int(o)
