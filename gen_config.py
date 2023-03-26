from fuzzingbook.Grammars import crange, srange, convert_ebnf_grammar, extend_grammar, is_valid_grammar
from fuzzingbook.Grammars import START_SYMBOL, new_symbol, Grammar
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
import os
import sys
import argparse

import json

BUILTIN_TYPES = {
    
}

def parse_grammar(filename: str) -> Grammar:
    data= {}
    with open(filename) as f:
        data = json.load(f)
    gram: Grammar = {}

    if data["bnf"]:
        gram = data
        del gram["bnf"]
    else:
        for k, v in BUILTIN_TYPES.items():
            gram[k] = v

        if "types" in data.keys():
            types = data["types"]
            for k, v in types.items():
                gram[k] = v

        opt_list = []

        for k, v in data["options"].items():
            opt_list.append(f"{k} {' '.join(v)}\n")
        gram["<start>"] = opt_list

    print(gram)
    return gram

def gen_config(grammar: Grammar, min_nonterminals: int) -> str:
    assert is_valid_grammar(grammar);

    ebnf= convert_ebnf_grammar(grammar)

    f = GrammarCoverageFuzzer(ebnf, min_nonterminals = min_nonterminals)

    config = ""

    for i in range(len(grammar["<start>"])):
        config += f.fuzz() 
    return config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", metavar='json file', type=str, help="path of configuration definition file")
    parser.add_argument("--num", "-n", type=int, default=1, help="# of configuration files being generated")
    parser.add_argument("--dest", "-d", type=str, default=None, help="destination to save configuration files")
    parser.add_argument("--min_nonterminals", "-m", type=int, default=1, help="# of non-terminals")
    args = parser.parse_args()

    grammar = parse_grammar(args.file)

    for i in range(args.num):
        config = gen_config(grammar, args.min_nonterminals)
        if args.dest is not None:
            with open(f"{args.dest}/config{i}.conf", "w") as f:
                f.write(config)
        print("===============================")
        print(config)