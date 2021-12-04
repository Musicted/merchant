import pytest

from src.merchant import Merchant


def test_trace1():
    """
    Ensure the output is correct for the given example trace
    :return: None
    """
    with open('trace_1_in', 'r') as f:
        lines_in = f.readlines()
    with open('trace_1_out', 'r') as f:
        lines_out = f.readlines()

    m = Merchant()
    for i, o in zip(lines_in, lines_out):
        assert m.read_string(i) == o.strip()

