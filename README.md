# My attempt at the 1 Billion row chaellenge using Python

Visit [https://1brc.dev/](https://1brc.dev/) to know more about the challenge (or to generate the 1 billion rows file, which is over `13Gb` in size).

My (currently) best performing solution is heavily based on [https://github.com/ifnesi/1brc/blob/main/calculateAverage.py](https://github.com/ifnesi/1brc/blob/main/calculateAverage.py).

My best score is (check Stats section for details): `33.01 s` (micro benchmark, this is measured on a single run, not a statistically significant solution).

Tested:

```bash
1- Laptop:

CPU: 11th Gen Intel® Core™ i7-11370H @ 3.30GHz × 8
RAM: 15.4 GiB

2- NVIDIA Jetson AGX Orin Developer Kit

CPU: 12-core Arm® Cortex®-A78AE v8.2 64-bit CPU 3MB L2 + 6MB L3 @ 2.2 GHz
RAM: 32 GB

---

Ubuntu 20.04.6 LTS
$ python --version  [Python 3.8.10]
$ pypy3 --version   [Python 3.6.9]
```

Stats:

- `chunks_pool.py`:
  * NVIDIA AGX Orin:
    + pypy: `33.01 s`
    + cpython: `75.59 s`
  * my laptop:
    + pypy: `49.59 s`
    + cpython: `139.09 s`

- `naive.py`:
  * pypy: `324.22 s`
  * cpython: `556.79 s`

- `naive_improv.py`:
  * pypy: `161.94 s`
  * cpython: `823.31 s`  # slow because of the cusom `bytes2int()` function
