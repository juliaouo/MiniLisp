import MiniLisp
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help="Input file")
    parser.add_argument('-s', action='store_true', default=False, help="Show Traceback")
    args = parser.parse_args()

    show_stack = args.s
    if not show_stack:
        sys.tracebacklimit = 0

    MiniLisp.MiniLispInterpreter().interpret(args.f)