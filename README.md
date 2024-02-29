# My attempt at the 1 Billion row chaellenge using Python

Visit [https://1brc.dev/](https://1brc.dev/) to know more about the challenge (or to generate the 1 billion rows file, which is over `10Gb` in size).

My (currently) best performing solution is heavily based on [https://github.com/ifnesi/1brc/blob/main/calculateAverage.py](https://github.com/ifnesi/1brc/blob/main/calculateAverage.py).

My best score is: `143.46 s` (micro benchmark, this is measured on a single run, not a statistical sane solution).

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

naive.py: 556.79 s
naive_obj.py: 
prod_cons.py: +oo
many_procs.py: 143.46