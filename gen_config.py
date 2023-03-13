from fuzzingbook.Grammars import crange, srange, convert_ebnf_grammar, extend_grammar, is_valid_grammar
from fuzzingbook.Grammars import START_SYMBOL, new_symbol, Grammar
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
import os
import sys

import json

BUILTIN_TYPES = {
    "<digit0>": crange("0", "9"),
    "<digit>": crange("1", "9"),
    "<integer>": ["0", "<digit><digit0>+"],
    "<bool>": ["true", "false"]
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

def gen_config(grammar: Grammar) -> str:
    assert is_valid_grammar(grammar);

    ebnf= convert_ebnf_grammar(grammar)

    f = GrammarCoverageFuzzer(ebnf, min_nonterminals = 1)

    config = ""

    for i in range(len(grammar["<start>"])):
        config += f.fuzz() 
    return config



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("missing config defenition file")
        exit(0)
    json_path = sys.argv[1]
    grammar = parse_grammar(json_path)

    for i in range(10):
        with open(f"config{i}.conf", "w") as f:
            config = gen_config(grammar)
            f.write(config)
            print("===============================")
            print(config)
            print("===============================")