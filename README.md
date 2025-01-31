[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mdusFg9r)
# search
Empirical and theoretic comparison of search methods.

## Usage
### Emperical comparison Experiment 1
```
usage: search.py [-h] --experiment_number NUMBER --query_percent PERCENT [--database_range DATABASE_RANGE DATABASE_RANGE DATABASE_RANGE] [--values_file VALUES_FILE] [--max_value MAX_VALUE] [--rounds ROUNDS] --out_file OUT_FILE 


optional arguments:
  -h, --help            show this help message and exit
  --database_range DATABASE_RANGE DATABASE_RANGE DATABASE_RANGE
                        Database range (start, stop, step) 
                            leave blank for experiment 2 (Default is 20,000
  --database_size DATABASE_SIZE
                        Database size
  --values_file VALUES_FILE
                        A gziped text file containing values to use for database and queries
  --max_value MAX_VALUE
                        Maximum value when searching integers (default: 235976)
  --rounds ROUNDS       Number of rounds to run each algorithm (default: 10)
  --out_file OUT_FILE   File to save plot to
```

## Example Experiment 1
```
$ python src/search.py \
    --experiment_number 1 \
    --query_percent 10 \
    --database_range 100 20000 2000 \
    --values_file ./data/words.txt.gz \
    --rounds 30 \
    --out_file ../doc/db100-20000-200qp10.png 
Binary search Time min 407483.0333333333 max 187627198.76666668
Merge search Time min 389542.73333333334 max 140508460.76666668
Hash table search Time min 91742.0 max 45307579.5
Binary search Memory min 8859.733333333334 max 1714252.0
Merge search Memory min 12760.533333333333 max 2303483.2
Hash table search Memory min 15688.0 max 2477612.0
```
<center><img src="/doc/db100-20000-200qp10.png" width="600"/></center>

## Example Experiment 2
```
$ python ./src/search.py \
    --experiment_number 2 \
    --query_percent 90 \
    --values_file ./data/words.txt.gz \
    --rounds 30 \
    --out_file ../doc/db20000_qp90_r30.png
Binary search Time min 7142864.066666666 max 22955407.7
Merge search Time min 5832611.633333334 max 21315806.933333334
Hash table search Time min 3101845.566666667 max 5463796.466666667
Binary search Memory min 238070.13333333333 max 382042.93333333335
Merge search Memory min 238070.13333333333 max 382042.93333333335
Hash table search Memory min 1044840.0 max 1188812.0
```

<center><img src="/doc/db20000_qp90_r30.png" width="600"/></center>


