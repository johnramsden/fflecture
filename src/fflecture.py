#!/usr/bin/env python

import subprocess as sp
import argparse


class Editor:
    FFMPEG_BIN = "ffmpeg"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create lecture with ffmpeg.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


def main():
    parse_arguments()


if __name__ == "__main__":
    main()
