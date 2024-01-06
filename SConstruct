import os
import os.path
import logging
import random
import subprocess
import shlex
import gzip
import re
import functools
import time
import imp
import sys
import json
#from steamroller import Environment

# workaround needed to fix bug with SCons and the pickle module
del sys.modules['pickle']
sys.modules['pickle'] = imp.load_module('pickle', *imp.find_module('pickle'))
import pickle

# actual variable and environment objects
vars = Variables("custom.py")
vars.AddVariables(
    ("OUTPUT_WIDTH", "", 5000),
    ("RANDOM_SEED", "", 0),
    ("DATA_PATH", "", os.path.expanduser("~/corpora")),
    ("ADAPTOR_GRAMMAR_PATH", "", os.path.expanduser("~/projects/py-cfg")),
)

env = Environment(
    variables=vars,
    ENV=os.environ,
    TARFLAGS="-c -z",
    TARSUFFIX=".tgz",
    tools=[],
    BUILDERS={
        "NormalizeChaucer" : Builder(
            action="python scripts/normalize_chaucer.py --input ${SOURCES[0]} --output ${TARGETS[0]}"
        ),
        "NormalizeForBetterForVerse" : Builder(
            action="python scripts/normalize_for_better_for_verse.py --input ${SOURCES[0]} --output ${TARGETS[0]}"
        ),        
        "TrainAdaptorGrammar" : Builder(
            action="${ADAPTOR_GRAMMAR_PATH}/py-cfg ${SOURCES[0]} -d 100 -r ${SEED} -P -n ${ITERATIONS} -G ${TARGETS[0]} -A ${TARGETS[1]} < ${SOURCES[1]}"
        ),
        "ParseAdaptorGrammar" : Builder(
            action="python scripts/parse_adaptor_grammar.py --grammar ${SOURCES[0]} --parses ${SOURCES[1]} --output ${TARGETS[0]}"
        )
    }
)

# function for width-aware printing of commands
def print_cmd_line(s, target, source, env):
    if len(s) > int(env["OUTPUT_WIDTH"]):
        print(s[:int(float(env["OUTPUT_WIDTH"]) / 2) - 2] + "..." + s[-int(float(env["OUTPUT_WIDTH"]) / 2) + 1:])
    else:
        print(s)

# and the command-printing function
env['PRINT_CMD_LINE_FUNC'] = print_cmd_line

# and how we decide if a dependency is out of date
env.Decider("timestamp-newer")

#chaucer = env.NormalizeChaucer(
#    "work/chaucer.jsonl.gz",
#    "data/chaucer.json.gz"
#)

fbfv = env.NormalizeForBetterForVerse(
    "work/fbfv.txt",
    "${DATA_PATH}/verse/for_better_for_verse.tgz"
)

chaucer = env.NormalizeChaucer(
    "work/chaucer.txt",
    "${DATA_PATH}/verse/chaucer.json.gz"
)

gram, parses = env.TrainAdaptorGrammar(
    ["work/chaucer_grammar.txt", "work/chaucer_parses.txt"],
    ["data/grammar.txt", chaucer],
    ITERATIONS=200,
    SEED=0
)

result = env.ParseAdaptorGrammar(
    "work/chaucer_result.txt",
    [gram, parses]
)

gram, parses = env.TrainAdaptorGrammar(
    ["work/fbfv_grammar.txt", "work/fbfv_parses.txt"],
    ["data/grammar.txt", fbfv],
    ITERATIONS=200,
    SEED=0
)

result = env.ParseAdaptorGrammar(
    "work/fbfv_result.txt",
    [gram, parses]
)
