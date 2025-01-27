[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mdusFg9r)
# search
Empirical and theoretic comparison of search methods.

## Usage
### Emperical comparison
```
usage: search.py [-h] --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE --database_size DATABASE_SIZE [--values_file VALUES_FILE] [--max_value MAX_VALUE] [--rounds ROUNDS] --out_file OUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE
                        Query size parameters (start stop step)
  --database_size DATABASE_SIZE
                        Database size
  --values_file VALUES_FILE
                        A gziped text file containing values to use for database and queries
  --max_value MAX_VALUE
                        Maximum value when searching integers (default: 235976)
  --rounds ROUNDS       Number of rounds to run each algorithm (default: 10)
  --out_file OUT_FILE   File to save plot to
```

### Theoretic comparison
```
usage: sim.py [-h] --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE --database_size DATABASE_SIZE --out_file OUT_FILE [--width WIDTH] [--height HEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  --query_range QUERY_RANGE QUERY_RANGE QUERY_RANGE
                        Query size parameters (start stop step)
  --database_size DATABASE_SIZE
                        Database size
  --out_file OUT_FILE   Output file
  --width WIDTH         Width of plot in inches (default: 3)
  --height HEIGHT       Height of plot in inches (default: 3)
```

## Example
```
python src/search.py \
    --query_range 100 200000 10000 \
    --database_size 200000  \
    --rounds 5 \
    --values_file data/words.txt.gz \
    --out_file doc/q100-10000_d200000_str.png
Binary search Time min 49883191.8 max 185743625.2
Merge search Time min 91795216.6 max 155866725.0
Hash table search Time min 18268700.0 max 35677233.4
Binary search Memory min 2397976.0 max 4564396.0
Merge search Memory min 2397976.0 max 4564376.0
Hash table search Memory min 17329544.0 max 18849516.0
```
<center><img src="/doc/q100-10000_d200000_str.png" width="600"/></center>

```
python sim.py \
    --query_range 100 200000 10000 \
    --database_size 200000  \
    --width 5 \
    --height 4 \
    --out_file ../doc/q100-10000_d200000_sim.png 
```
<center><img src="/doc/q100-10000_d200000_sim.png" width="600"/></center>


