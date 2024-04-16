# Ref: https://github.com/ifnesi/1brc/blob/main/calculateAverage.py
# pypy: 49.59 s
# cpython: 139.09 s

from collections import defaultdict
import multiprocessing as mp
import time
import os

from utils import bytes2int

from typing import Tuple, DefaultDict, List, Union
Chunks = List[Tuple[str, int, int]]


NEWLINE = b'\n'
MIN, MAX, SUM, COUNT = (0, 1, 2, 3)


def default_list() -> List[Union[float, int]]:
    # min, max, sum, count
    return [99.0, -99.0, 0.0, 1]


def get_file_chunks(file_path: str, n_cpu: int = 8) -> Chunks:

    def is_new_line(pos):
        if pos == 0:
            return True

        fp.seek(pos - 1)
        return fp.read(1) == NEWLINE

    file_sz: int = os.stat(file_path).st_size
    chunk_sz: int = file_sz // n_cpu

    chunks: Chunks = []

    with open(file_path, "rb") as fp:

        start = 0
        while start < file_sz:
            end = min(file_sz, start + chunk_sz)

            while not is_new_line(end):
                end -= 1

            if end == start:
                fp.seek(end)
                fp.readline()
                end = fp.tell()

            chunks.append((file_path, start, end))
            start = end
        
    return chunks


def process_chunk(
        file_path: str, start: int, end: int
    ) -> DefaultDict[str, List[Union[float, int]]]:

    res = defaultdict(default_list)

    with open(file_path, 'rb') as fp:
        fp.seek(start)
        for line in fp:
            start += len(line)
            if start > end:
                break

            idx = line.find(b";")
            city = line[:idx]

            # Do all processing with ints, then only change to floats when printing the resutls
            val = bytes2int(line[idx + 1:])
            # val = int(line[idx + 1:-3] + line[-2:-1])

            vals = res[city]
            if val < vals[MIN]:
                vals[MIN] = val
            elif val > vals[MAX]:
                vals[MAX] = val
            vals[SUM] += val
            vals[COUNT] += 1

    return res


def process_file(chunks: List[Tuple[int, int]], n_cpu: int = 8):
    with mp.Pool(n_cpu) as p:
        chunk_results = p.starmap(process_chunk, chunks)

        db: DefaultDict[str, List[float]] = defaultdict(default_list)
        for res in chunk_results:
            for city, vals in res.items():

                city_vals = db[city]
                if vals[MIN] < city_vals[MIN]:
                    city_vals[MIN] = vals[MIN]
                elif vals[MAX] > city_vals[MAX]:
                    city_vals[MAX] = vals[MAX]

                city_vals[SUM] += vals[SUM]
                city_vals[COUNT] += vals[COUNT]

    print("{", end="")
    city: bytes
    vals: List[int]
    for city, vals in sorted(db.items()):
        print(f"{city.decode()}={0.1 * vals[MIN]:.1f}/{0.1 * (vals[SUM] / vals[COUNT]):.1f}/{0.1 * vals[MAX]:.1f}", end=", ")
    print("\b\b} ")


if __name__ == '__main__':
    n_cpu = mp.cpu_count()

    file_path = 'measurements.txt'


    ts: float = time.perf_counter()

    chunks = get_file_chunks(file_path, n_cpu)
    process_file(chunks, n_cpu)

    print(f"{time.perf_counter() - ts:.2f} s")
