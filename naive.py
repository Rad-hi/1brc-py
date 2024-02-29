# 557.63 s

from collections import defaultdict
import time

from typing import DefaultDict, List


MIN, MAX, SUM, COUNT = (0, 1, 2, 3)
empty_list = lambda: [99.0, -99.0, 0.0, 1]
db: DefaultDict[str, List[int]] = defaultdict(empty_list)


if __name__ == '__main__':
    PATH = 'measurements.txt'

    ts: float = time.perf_counter()

    with open(PATH, 'r') as f:
        for line in f:
            city, val = line[:-1].split(';')

            val = float(val)

            vals = db[city]
            if val < vals[MIN]:
                vals[MIN] = val
            elif val > vals[MAX]:
                vals[MAX] = val

            vals[SUM] += val
            vals[COUNT] += 1

    print("{", end="")
    for city, vals in sorted(db.items()):
        print(f"{city}={vals[MIN]:.1f}/{(vals[SUM] / vals[COUNT])}/{vals[MAX]:.1f}", end=", ")
    print("\b\b} ")

    print(f"{time.perf_counter() - ts:.2f} s")
