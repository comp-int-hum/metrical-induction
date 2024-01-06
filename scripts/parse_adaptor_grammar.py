import argparse
import gzip
import re
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--grammar", dest="grammar", help="Input file")
    parser.add_argument("--parses", dest="parses", help="Input file")
    parser.add_argument("--output", dest="output", help="Output file")
    args = parser.parse_args()

    feet = {}
    with open(args.grammar, "rt") as ifd:
        for line in ifd:
            if line.startswith("("):
                foot = re.sub(r"\#\d+", "", line.strip())
                feet[foot] = feet.get(foot, 0) + 1
    for count, foot in sorted([(v, k) for k, v in feet.items()]):
        print(count, foot)
