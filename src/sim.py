import argparse
import math
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query_range',
                        type=int,
                        required=True,
                        nargs=3,
                        help='Query size parameters (start stop step)')
    parser.add_argument('--database_size',
                        type=int,
                        required=True,
                        help='Database size')
    parser.add_argument('--out_file',
                        type=str,
                        required=True,
                        help='Output file')
    parser.add_argument('--width',
                        type=float,
                        default=3,
                        help='Width of plot in inches (default: 3)')
    parser.add_argument('--height',
                        type=float,
                        default=3,
                        help='Height of plot in inches (default: 3)')
    return parser.parse_args()

def binary_search_rt(q, d):
    return d*math.log(q) + q*math.log(d)
def merge_search_rt(q, d):
    return d*math.log(q) + q*math.log(q) + q + d

def main():
    args = get_args()

    binary_search_rts = []
    merge_search_rts = []

    for q_size in range(args.query_range[0],
                    args.query_range[1],
                    args.query_range[2]):
        binary_search_rts.append(binary_search_rt(q_size, args.database_size))
        merge_search_rts.append(merge_search_rt(q_size, args.database_size))

    fig, ax = plt.subplots(figsize=(args.width, args.height))
    ax.plot(range(args.query_range[0],
                   args.query_range[1],
                   args.query_range[2]),
            binary_search_rts,
            label='Binary Search')
    ax.plot(range(args.query_range[0],
                   args.query_range[1],
                   args.query_range[2]),
            merge_search_rts,
            label='Merge Search')
    ax.set_xlabel('Query Size')
    ax.set_ylabel('Runtime')
    ax.set_title('Runtime vs. Query Size')
    ax.legend(loc='best', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    fig.savefig(args.out_file)


if __name__ == '__main__':
    main()
