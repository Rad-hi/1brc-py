import time

from typing import Dict


class Record:
    def __init__(self, mn, mx, sm, cnt) -> None:
        self.min = mn
        self.max = mx
        self.sum = sm
        self.cnt = cnt
        self.avg = 0


MIN, MAX, SUM, COUNT = (0, 1, 2, 3)
db: Dict[str, Record] = {}


def update_db(line: str) -> None:
    global db
    city, val = line[:-1].split(';')
    val = float(val)

    if city not in db:
        db[city] = Record(0, 0, 0, 0)

    mn = db[city].min
    mx = db[city].max
    sm = db[city].sum
    cn = db[city].cnt

    db[city] = Record(
        val if val < mn else mn,
        val if val > mx else mx,
        sm + val,
        cn + 1
    )


def main(path: str) -> None:
    with open(path, 'r') as f:
        for line in f:
            update_db(line)

    print("{", end="")
    for city, vals in sorted(db.items()):
        print(f"{city}={vals[MIN]:.1f}/{(vals[SUM] / vals[COUNT])}/{vals[MAX]:.1f}", end=", ")
    print("\b\b} ")


if __name__ == '__main__':
    PATH = 'measurements.txt'

    ts: float = time.perf_counter()
    main(PATH)
    print(f"{time.perf_counter() - ts:.2f} s")