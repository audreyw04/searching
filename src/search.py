import argparse
import bisect
import random
import gzip
import time
import numpy as np
import matplotlib.pyplot as plt
import tracemalloc

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_number',
                        type=int,
                        required=True,
                        help='Experiment 1: fixed query ratio and incrimental database size'
                            + 'Experiment 2: fixed database size (for experiment 2, leave database blank')
    parser.add_argument('--query_percent',
                        type=float,
                        required=True,
                        help='Query size as percent of database size (as whole number)'
                            + 'For Experiment 2: this is max percentage (10 incriments to 0)')
    parser.add_argument('--database_range',
                        type=int,
                        nargs=3,
                        help='Database range (start, stop, step) '
                            + 'leave blank for experiment 2 (Default is 20,000')
    parser.add_argument('--values_file',
                        type=str,
                        help='A gziped text file containing values to ' \
                             + 'use for database and queries')
    parser.add_argument('--max_value',
                        type=int,
                        default=235976,
                        help='Maximum value when searching integers ' \
                             + '(default: 235976)')
    parser.add_argument('--rounds',
                        type=int,
                        default=10,
                        help='Number of rounds to run each algorithm ' \
                             + '(default: 10)')
    parser.add_argument('--out_file',
                        type=str,
                        required=True,
                        help='File to save plot to')
    parser.add_argument('--width',
                        type=float,
                        default=8,
                        help='Width of plot in inches (default: 8)')
    parser.add_argument('--height',
                        type=float,
                        default=5,
                        help='Height of plot in inches (default: 5)')
    return parser.parse_args()

def read_values_file(file_name):
    V = [] 
    with gzip.open(file_name, 'rt') as f:
        for line in f:
            V.append(line.rstrip())
    return V

def get_rand_ints(N, min_v, max_v):
    rand_ints = []

    for _ in range(N):
        rand_int = random.randint(min_v, max_v)
        rand_ints.append(rand_int)

    return rand_ints

def binary_search(Q, D):
    D.sort()
    found = []
    for q in Q:
        index = bisect.bisect_left(D, q)
        if index < len(D) and D[index] == q:
            found.append(q)
    return len(found)

def merge_search(Q, D):
    found = []

    Q.sort()
    D.sort()

    q_i = 0
    d_i = 0

    while q_i < len(Q) and d_i < len(D):
        if Q[q_i] == D[d_i]:
            found.append(Q[q_i])
            q_i += 1
            d_i += 1
        elif Q[q_i] < D[d_i]:
            q_i += 1
        else:
            d_i += 1
    return len(found)

def hash_table(Q, D):
    found = []
    H = {}
    for d in D:
        H[d] = 1
    for q in Q:
        if q in H:
            found.append(q)
    return len(found)

def get_db_queries(num_database, num_queries, max_value=None, V=None):
    D = None
    Q = None

    if V is not None:
        D = random.sample(V, num_database)
        Q = random.sample(V, num_queries)
    elif max_value is not None:
        D = get_rand_ints(num_database, 0, max_value)
        Q = get_rand_ints(num_queries, 0, max_value)

    return D, Q

def plot_result(x_values, binary_search_mean_times, merge_search_mean_times, hash_table_search_mean_times, binary_search_mean_mems, merge_search_mean_mems, hash_table_search_mean_mems, args):
    fig, axs = plt.subplots(2,1, figsize=(args.width, args.height))

    ax = axs[0]
    ax.plot(x_values,
            binary_search_mean_times,
            label='Binary search')
    print('Binary search',
          'Time',
          'min', min(binary_search_mean_times),
          'max', max(binary_search_mean_times))

    ax.plot(x_values,
            merge_search_mean_times,
            label='Merge search')
    print('Merge search',
          'Time',
          'min', min(merge_search_mean_times),
          'max', max(merge_search_mean_times))

    ax.plot(x_values,
            hash_table_search_mean_times,
            label='Hash table search')
    print('Hash table search',
          'Time',
          'min', min(hash_table_search_mean_times),
          'max', max(hash_table_search_mean_times))

    ax.set(ylabel='Time (ns)',
           title=f'Search algorithms (database size: {args.database_range})')
    ax.set_xticklabels([])
    ax.legend(loc='best', frameon=False, ncol=3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax = axs[1]
    ax.plot(x_values,
            binary_search_mean_mems,
            label='Binary search')
    print('Binary search',
          'Memory',
          'min', min(binary_search_mean_mems),
          'max', max(binary_search_mean_mems))
    ax.plot(x_values,
            merge_search_mean_mems,
            label='Merge search')

    print('Merge search',
          'Memory',
          'min', min(merge_search_mean_mems),
          'max', max(merge_search_mean_mems))

    ax.plot(x_values,
            hash_table_search_mean_mems,
            label='Hash table search')
    print('Hash table search',
          'Memory',
          'min', min(hash_table_search_mean_mems),
          'max', max(hash_table_search_mean_mems))

    ax.set(xlabel='Query size',
           ylabel='Memory (bytes)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    fig.savefig(args.out_file)

def experiment_1(args, V):
    qr = args.query_percent

    binary_search_mean_times = []
    merge_search_mean_times = []
    hash_table_search_mean_times = []

    binary_search_mean_mems = []
    merge_search_mean_mems = []
    hash_table_search_mean_mems = []

    database_sizes = range(args.database_range[0], args.database_range[1], args.database_range[2])

    for db_size in database_sizes:

        binary_search_times = []
        merge_search_times = []
        hash_table_search_times = []

        binary_search_mems = []
        merge_search_mems = []
        hash_table_search_mems = []

        for _ in range(args.rounds):
            D, Q = get_db_queries(db_size, int(db_size * qr), args.max_value, V=V)

            start = time.monotonic_ns()
            ss_found = binary_search(Q.copy(), D.copy())
            stop = time.monotonic_ns()
            binary_search_times.append(stop - start)


            tracemalloc.start()
            ss_found = binary_search(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            binary_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()


            start = time.monotonic_ns()
            ms_found = merge_search(Q.copy(), D.copy())
            stop = time.monotonic_ns()
            merge_search_times.append(stop - start)

            tracemalloc.start()
            ms_found = merge_search(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            merge_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()


            ht_start = time.monotonic_ns()
            ht_found = hash_table(Q.copy(), D.copy())
            ht_stop = time.monotonic_ns()
            hash_table_search_times.append(ht_stop - ht_start)

            tracemalloc.start()
            ht_found = hash_table(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            hash_table_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()

            #assert(ss_found == ms_found)
            #assert(ss_found == ht_found)

        binary_search_mean_times.append(np.mean(binary_search_times))
        merge_search_mean_times.append(np.mean(merge_search_times))
        hash_table_search_mean_times.append(np.mean(hash_table_search_times))

        binary_search_mean_mems.append(np.mean(binary_search_mems))
        merge_search_mean_mems.append(np.mean(merge_search_mems))
        hash_table_search_mean_mems.append(np.mean(hash_table_search_mems))

    plot_result(database_sizes, binary_search_mean_times, merge_search_mean_times, hash_table_search_mean_times, binary_search_mean_mems, merge_search_mean_mems, hash_table_search_mean_mems, args)


def experiment_2(args, V):
    database_size = 20000
    qp = args.query_percent /100
    query_sizes = [int(database_size * (qp * i / 10)) for i in range(11)]

    binary_search_mean_times = []
    merge_search_mean_times = []
    hash_table_search_mean_times = []

    binary_search_mean_mems = []
    merge_search_mean_mems = []
    hash_table_search_mean_mems = []

    for query_size in query_sizes:
        binary_search_times = []
        merge_search_times = []
        hash_table_search_times = []

        binary_search_mems = []
        merge_search_mems = []
        hash_table_search_mems = []

        for _ in range(args.rounds):
            D, Q = get_db_queries(database_size, query_size, args.max_value, V=V)

            start = time.monotonic_ns()
            ss_found = binary_search(Q.copy(), D.copy())
            stop = time.monotonic_ns()
            binary_search_times.append(stop - start)


            tracemalloc.start()
            ss_found = binary_search(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            binary_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()


            start = time.monotonic_ns()
            ms_found = merge_search(Q.copy(), D.copy())
            stop = time.monotonic_ns()
            merge_search_times.append(stop - start)

            tracemalloc.start()
            ms_found = merge_search(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            merge_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()


            ht_start = time.monotonic_ns()
            ht_found = hash_table(Q.copy(), D.copy())
            ht_stop = time.monotonic_ns()
            hash_table_search_times.append(ht_stop - ht_start)

            tracemalloc.start()
            ht_found = hash_table(Q.copy(), D.copy())
            mem = tracemalloc.get_traced_memory()
            hash_table_search_mems.append(mem[1] - mem[0])
            tracemalloc.stop()

            #assert(ss_found == ms_found)
            #assert(ss_found == ht_found)

        binary_search_mean_times.append(np.mean(binary_search_times))
        merge_search_mean_times.append(np.mean(merge_search_times))
        hash_table_search_mean_times.append(np.mean(hash_table_search_times))

        binary_search_mean_mems.append(np.mean(binary_search_mems))
        merge_search_mean_mems.append(np.mean(merge_search_mems))
        hash_table_search_mean_mems.append(np.mean(hash_table_search_mems))

    plot_result(query_sizes, binary_search_mean_times, merge_search_mean_times, hash_table_search_mean_times, binary_search_mean_mems, merge_search_mean_mems, hash_table_search_mean_mems, args)




def main():
    args = get_args()

    V = None
    if args.values_file:
        V = read_values_file(args.values_file)

    if args.experiment_number == 1:
        experiment_1(args, V)
    elif args.experiment_number == 2:
        experiment_2(args, V)



    
if __name__ == '__main__':
    main()
