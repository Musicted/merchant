from merchantsguide.merchant import Merchant


def test_trace1():
    """
    Ensure the output is correct for the given example trace
    :return: None
    """
    with open('merchantsguide/tests/end2end/trace_1_in', 'r') as f:
        lines_in = f.readlines()
    with open('merchantsguide/tests/end2end/trace_1_out', 'r') as f:
        lines_out = f.readlines()

    m = Merchant()
    for i, o in zip(lines_in, lines_out):
        res = m.single_command(i)
        if o:
            assert res == o

