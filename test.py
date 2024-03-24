from utils import str2f

def test_str2f():
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

    for in_, gt in zip(ins, gts):
        out = str2f(in_)
        assert out == gt


import time

in_ = '-12.5'

ts = time.perf_counter()
str2f(in_)
tss = time.perf_counter() - ts
print(f'{tss * 1000_000.0} us')

ts = time.perf_counter()
float(in_)
tss = time.perf_counter() - ts
print(f'{tss * 1000_000.0} us')