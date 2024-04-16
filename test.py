from utils import str2f, bytes2int

ins = [
    '-12.2\n',
    '12.2\n',
    '-2.9\n',
    '2.9\n',
    '-12.2',
    '12.2',
    '-2.9',
    '2.9',
]

gts = [
    -12.2,
    12.2,
    -2.9,
    2.9,
    -12.2,
    12.2,
    -2.9,
    2.9,
]


def test_str2f():
    for in_, gt in zip(ins, gts):
        out = str2f(in_)
        assert out == gt
    print('PASSED: [test_str2f]')


def test_b2i():
    for in_, gt in zip(ins, gts):
        out = bytes2int(in_.encode())
        assert abs((0.1 * out) - gt) < 0.1
    print('PASSED: [test_b2i]')


test_str2f()
test_b2i()