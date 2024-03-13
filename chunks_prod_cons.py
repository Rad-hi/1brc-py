# Ref: https://github.com/ifnesi/1brc/blob/main/calculateAverage.py
# 

from collections import defaultdict
import multiprocessing as mp
from threading import Thread 
import time
import os

from typing import Tuple, DefaultDict, List, Union

Chunks = List[Tuple[str, int, int]]


NEWLINE = b'\n'
MIN, MAX, SUM, COUNT = (0, 1, 2, 3)
MAX_N_CPU: int = 8

proc_list: List[Tuple[mp.Process, mp.Queue, mp.Event]] = []


def default_list() -> List[Union[float, int]]:
    # min, max, sum, count
    return [99.0, -99.0, 0.0, 1]

db: DefaultDict[str, List[float]] = defaultdict(default_list)


def process_chunk(
        file_path: str, start: int, end: int, q: mp.Queue, e: mp.Event,
    ) -> DefaultDict[str, List[Union[float, int]]]:

    with open(file_path, 'r') as fp:
        fp.seek(start)
        for line in fp:
            start += len(line)
            if start > end:
                break

            city, val = line.split(';')
            val = float(val)
            q.put((city, val))
    print('done')
    e.set()


def launch_chunks_processors(file_path: str, n_cpu: int = 8) -> Chunks:
    def is_new_line(pos):
        if pos == 0:
            return True
        fp.seek(pos - 1)
        return fp.read(1) == NEWLINE

    global proc_list

    if n_cpu > MAX_N_CPU:
        n_cpu = MAX_N_CPU

    file_sz: int = os.stat(file_path).st_size
    chunk_sz: int = file_sz // n_cpu

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

            q = mp.Queue(maxsize=2_000_000)
            e = mp.Event()
            e.clear()
            proc = mp.Process(target=process_chunk, args=(file_path, start, end, q, e))
            proc.start()
            proc_list.append((proc, q, e))

            start = end


def single_proc_res_accum_thread(q: mp.Queue, e: mp.Event):
    global db

    while not e.is_set():
        try:
            city, val = q.get_nowait()
            # print(city, val, q.qsize())
        except:
            # Empty queue
            continue

        vals = db[city]
        if val < vals[MIN]:
            vals[MIN] = val
        elif val > vals[MAX]:
            vals[MAX] = val

        vals[SUM] += val
        vals[COUNT] += 1

def result_accumulator():
    
    th_l: List[Thread] = []
    for _, q, e in proc_list:
        th = Thread(target=single_proc_res_accum_thread, args=(q, e))
        th.start()
        th_l.append(th)

    for th in th_l:
        th.join()

    for p, _, _ in proc_list:
        p.join()

    print("{", end="")
    for city, vals in sorted(db.items()):
        print(f"{city}={vals[MIN]:.1f}/{(vals[SUM] / vals[COUNT])}/{vals[MAX]:.1f}", end=", ")
    print("\b\b} ")


if __name__ == '__main__':
    n_cpu = mp.cpu_count()

    file_path = 'measurements.txt'

    ts: float = time.perf_counter()

    launch_chunks_processors(file_path, n_cpu)
    result_accumulator()


    print(f"{time.perf_counter() - ts:.2f} s")
