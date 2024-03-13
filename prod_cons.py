from multiprocessing import Process, SimpleQueue, Event
from tqdm import tqdm
import time


FILE_PATH = 'measurements.txt'
WORKERS = 8

MIN, MAX, SUM, COUNT= (0, 1, 2, 3)


def db_updater(e, db, q)-> None:
    while True:
        line = q.get()
        city, val = line[:-1].split(';')
        if city not in db:
            db[city] = [99.0, -99.0, 0.0, 1]

        val = float(val)

        if val < db[city][MIN]:
            db[city][MIN] = val
        elif val > db[city][MAX]:
            db[city][MAX] = val

        db[city][SUM] += val
        db[city][COUNT] += 1

        if q.empty() and e.is_set():
            break


def file_reader(e, qs) -> None:
    with open(FILE_PATH, 'r') as f:
        for line in tqdm(f):
            qs[hash(line) % WORKERS].put(line)
    e.set()


def main():
    e = Event()
    db = dict()

    qs = [SimpleQueue()] * WORKERS
    reader = Process(target=file_reader, args=(e, qs))
    updaters = [Process(target=db_updater, args=(e, db, qs[i])) for i in range(WORKERS)]

    for updater in updaters:
        updater.start()
    reader.start()

    reader.join()
    for updater in updaters:
        updater.join()

    print("{", end="")
    for city, vals in sorted(db.items()):
        print(f"{city}={vals[MIN]:.1f}/{(vals[SUM] / vals[COUNT])}/{vals[MAX]:.1f}", end=", ")
    print("\b\b} ")



if __name__ == '__main__':
    ts = time.perf_counter()
    main()
    print(f"{time.perf_counter() - ts:.2f} s")
