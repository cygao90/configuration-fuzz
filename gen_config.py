from fuzzingbook.Grammars import crange, srange, convert_ebnf_grammar, extend_grammar, is_valid_grammar
from fuzzingbook.Grammars import START_SYMBOL, new_symbol, Grammar
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
import os
import sys

import json

def parse_grammar(filename: str) -> Grammar:
    data= {}
    with open(filename) as f:
        data = json.load(f)
    gram: Grammar = {}
    if data["bnf"]:
        gram = data
        del gram["bnf"]
    else:
        type_set = data["values"]
        gram["<start>"] = []
        for k, v in data["values"].items():
            gram[k] = v
        for k, v in data["opts"].items():
            if k in type_set:
                for item in v:
                    gram["<start>"].append(f"{item} {k}\n") 
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
    json_path = sys.argv[1]
    grammar = parse_grammar(json_path)

    for i in range(10):
        with open(f"config{i}.conf", "w") as f:
            config = gen_config(grammar)
            f.write(config)
            print("===============================")
            print(config)
            print("===============================")