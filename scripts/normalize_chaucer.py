import argparse
import json
import gzip

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Input file")
    parser.add_argument("-o", "--output", dest="output", help="Output file")
    args = parser.parse_args()

    with gzip.open(args.input, "rt") as ifd, open(args.output, "wt") as ofd:
        j = json.loads(ifd.read())
        for book_name, book in j.items():
            for line_num, line in book["content"].items():
                seq = []
                for word_num, word in sorted([(int(i), w) for i, w in line.items()]):
                    #print(word)
                    for syll_num, syll in sorted([(int(i), s) for i, s in word["syllables"].items()]):
                        mark = syll["scansion"]
                        if mark == "u":
                            seq.append("Unstress")
                        elif mark == "s":
                            seq.append("Stress")
                if len(seq) > 0:
                    ofd.write(" ".join(seq) + "\n")
