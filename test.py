from utils import str2f

def test_str2f():
    ins = [
        '-12.2\n',
        '12.2\n',
        '-2.9\n',
        '2.9\n',
    ]

    gts = [
        -12.2,
        12.2,
        -2.9,
        2.9,
    ]

    for in_, gt in zip(ins, gts):
        out = str2f(in_)
        assert out == gt
