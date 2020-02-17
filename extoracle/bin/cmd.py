#!/usr/bin/env python
import extoracle


def main():
    import argparse

    parser = argparse.ArgumentParser("Ext-Oracle Summarization")
    parser.add_argument("source",
                        help="Path to source file (one example per line)")
    parser.add_argument("target",
                        help="Path to target file (one example per line)")
    parser.add_argument("-method", "-m", default="greedy", choices=extoracle.METHODS,
                        help="""Ext-Oracle method (combination is more
                                accurate but takes much longer""")
    parser.add_argument("-length", "-l", type=int, default=None,
                        help="Length of summaries, in sentences")
    parser.add_argument("-length_oracle", action="store_true",
                        help="Use target summary length")
    parser.add_argument("-output", "-o", default=None,
                        help="""Path to output file
                                (default: print to stdout""")
    parser.add_argument("-trunc", "-t", default=None, type=int,
                        help="Truncate source to <= `trunc` words")

    args = parser.parse_args()

    extoracle.from_files(args.source, args.target, args.method,
                         output=args.output,
                         summary_length=args.length,
                         length_oracle=args.length_oracle,
                         trunc_src=args.trunc)


if __name__ == "__main__":
    main()
