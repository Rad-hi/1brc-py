# My attempt at the 1 Billion row chaellenge using Python

Visit [https://1brc.dev/](https://1brc.dev/) to know more about the challenge (or to generate the 1 billion rows file, which is over `10Gb` in size).

My (currently) best performing solution is heavily based on [https://github.com/ifnesi/1brc/blob/main/calculateAverage.py](https://github.com/ifnesi/1brc/blob/main/calculateAverage.py).

My best score is (check Stats section for details): `33.01 s` (micro benchmark, this is measured on a single run, not a statistical sane solution).

My system (tested on):

```bash

CPU: 11th Gen Intel® Core™ i7-11370H @ 3.30GHz × 8
GPU: NVIDIA GeForce GTX 1650
RAM: 15.4 GiB

Ubuntu 20.04.6 LTS

$ python --version
>>> Python 3.8.10

```

Stats:

- chunks_pool.py:
  * NVIDIA AGX Orin 32Gb:
    + pypy: `33.01 s`
    + cpython: `75.59 s`
  * my laptop:
    + pypy: `49.59 s`
    + cpython: `139.09 s`

- naive.py:
  * pypy: `324.22 s`
  * cpython: `556.79 s`

- naive_improv.py:
  * pypy: `161.94 s`
  * cpython: `823.31 s`  # slow because of the cusom `bytes2int()` function