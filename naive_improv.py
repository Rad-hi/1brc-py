# pypy: 161.94 s
# cpython: 823.31 s

from collections import defaultdict
import time

from utils import bytes2int

from typing import DefaultDict, List


MIN, MAX, SUM, COUNT = (0, 1, 2, 3)
empty_list = lambda: [99.0, -99.0, 0.0, 1]
db: DefaultDict[str, List[int]] = defaultdict(empty_list)


if __name__ == '__main__':
    PATH = 'measurements.txt'

    ts: float = time.perf_counter()

    with open(PATH, 'rb') as f:
        for line in f:

            idx = line.find(b";")
            city = line[:idx]
            val = bytes2int(line[idx + 1:])

            vals = db[city]
            if val < vals[MIN]:
                vals[MIN] = val
            elif val > vals[MAX]:
                vals[MAX] = val

            vals[SUM] += val
            vals[COUNT] += 1

    print("{", end="")
    city: bytes
    vals: List[int]
    for city, vals in sorted(db.items()):
        print(f"{city.decode()}={0.1 * vals[MIN]:.1f}/{0.1 * (vals[SUM] / vals[COUNT]):.1f}/{0.1 * vals[MAX]:.1f}", end=", ")
    print("\b\b} ")

    print(f"{time.perf_counter() - ts:.2f} s")
