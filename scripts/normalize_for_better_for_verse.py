import argparse
import gzip
import tarfile
import json
import xml.etree.ElementTree as et

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Input file")
    parser.add_argument("-o", "--output", dest="output", help="Output file")
    args = parser.parse_args()

    ns = {"tei" : "http://www.tei-c.org/ns/1.0"}
    
    with tarfile.open(args.input, "r") as ifd, open(args.output, "wt") as ofd:
        for member in ifd.getmembers():
            if member.isfile() and member.name.startswith("for_better_for_verse/poems/") and member.name.endswith("xml") and not "Poet" in member.name and not "test" in member.name and not "Gods" in member.name:
                xml = et.fromstring(ifd.extractfile(member).read())
                titles = [x.text for x in xml.findall("{*}teiHeader/{*}fileDesc/{*}titleStmt/{*}title")]
                authors = [x.text for x in xml.findall("{*}teiHeader/{*}fileDesc/{*}titleStmt/{*}author")]
                dates = [x.text for x in xml.findall("{*}teiHeader/{*}fileDesc/{*}publicationStmt/{*}date")]
                if len(dates) == 0:
                    dates = [x.text for x in xml.findall("{*}teiHeader/{*}fileDesc/{*}publicationStmt")]
                texts = xml.findall("{*}text/{*}body")
                assert len(texts) == 1
                
                for lg in texts[0].findall("{*}lg"):
                    # org sample part
                    tp = lg.get("type")
                    meter = lg.get("met")

                    rhyme = lg.get("rhyme")
                    # l[@real] seg rhyme[@label] sb caesura
                    for l in lg.findall("{*}l"):
                        seq = []
                        met = l.get("met")
                        rel = l.get("real").replace(" ", "").split("|") # alternate scans
                        for c in rel[0]:
                            if c == "-":
                                seq.append("Unstress")
                            elif c == "+":
                                seq.append("Stress")
                            elif c == "^":
                                seq.append("Unstress") # added fem.
                            elif c in ["(", ")"]:
                                pass
                            else:
                                raise Exception((member.name, c))
                        #seq.append("EndOfLine")                        
                        #for seg in l.findall("{*}seg"): # caesura
                        #    # seg > sb
                        #    met = l.get("met")
                        #    rel = l.get("real")
                        #    for rm in seg.findall("{*}rhyme"): # sb
                        #        lab = rm.get("label")
                        ofd.write(" ".join(seq) + "\n")
