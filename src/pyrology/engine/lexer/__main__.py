import argparse
import logging
import os
import yaml

from pyrology.utils import get_functor, get_name
from pyrology.engine.lexer.utils import sanitize_src, get_source, write_tokens
from pyrology.engine.lexer.rules import parse_rule

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class IgnisTokenizer:
    def __init__(self, source=None):
        self.source = source
        self.prepare()

    def prepare(self, source=None):
        if source:
            self.source = source

        self.rules = {}
        self.constants = set()
        self.relations = {}

        if self.source:
            self._tokenstream()

        return self.get_tokens()

    def add_rule(self, rule):
        name, args, goals = parse_rule(rule)

        if name not in self.rules:
            self.rules[name] = []

        self.rules[name].append({'src': rule, 'args': args, 'goals': goals})

    def add_fact(self, fact):
        try:
            functor, args = get_functor(fact)
            name = get_name(functor, args)
        except TypeError:
            return  # Or break - phantom term is coming up.

        if name not in self.relations:
            self.relations[name] = []

        self.relations[name].append(args)
        self.constants.update(args)

    def _tokenstream(self):
        """
        Get a token stream from a source str.

        All ye who enter here, just **beware**.
        Nothing about this is an actual tokenizer, it just produces some 
        usable token stream and partially initialized environment state
        for the parser-engine to grok.

        We have rules and facts, and we tokenize them in separate passes.
        relations are inferred from facts, and rules are iteratively defined.

        The global constant dictionary is created from the set of all
        lowercase `functor(a1, a2, a3[, ...])` tokens in the source str. 

        Constants are used as unique types for the parser-engine.

        relation(atom, <...>).
        rule(VARIABLE, <...>) :- relation(VARIABLE, <...>)[;,] <...>.
        """
        sanitized = sanitize_src(self.source)
        statements = sanitized.split('.')

        # Generate rule tokens.
        for rule in filter(lambda s: ':-' in s, statements):
            self.add_rule(rule)
        
        # Get all constants from facts.

        for fact in filter(lambda s: ':-' not in s and s != '', statements):
            self.add_fact(fact)

    def get_tokens(self):
        return {
            'constants': self.constants,
            'relations': self.relations,
            'rules': self.rules,
        }


def main():
    parser = argparse.ArgumentParser(description="Tokenize a source file.")
    parser.add_argument('script', type=str,
                        help="The source file to tokenize.")
    args = parser.parse_args()

    path = args.script
    name = os.path.basename(path).split('.')[0]

    source = get_source(path)
    tokenizer = IgnisTokenizer(source)
    tokened = tokenizer.get_tokens()

    yml = write_tokens(tokened, f"output/{name}.yaml")
