import argparse
from multiprocessing.sharedctypes import Value
import os
import time
import yaml


def write_tokens(tokens, filename):
    """Write tokens to a file and returns the YAML object."""
    if not os.path.exists("output"):
        os.mkdir("output")

    with open(filename, 'w') as f:
        yml = yaml.dump(tokens)
        f.write(yml)

    return yml


def get_source(path):
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    else:
        print(f"No such file: {path}")

TOKENS = ['(', ')', ',', ';', ':-', '.']

def tokenize(statement):
    """Tokenize a statement."""
    tokens = []
    for c in statement:
        if c in TOKENS:
            tokens.append(c)
        else:
            if tokens and tokens[-1] not in TOKENS:
                tokens[-1] += c
            else:
                tokens.append(c)

    return tokens


def get_first_comma_not_in_parens(string):
    """Get the index of the first comma not in parentheses."""
    parens = 0
    for i, c in enumerate(string):
        if c == '(':
            parens += 1
        elif c == ')':
            parens -= 1
        elif c == ',' and parens == 0:
            return i


def rule_munch(body):
    goals = []
    while True:
        first_comma = get_first_comma_not_in_parens(body) or len(body)
        try:
            first_semicolon = body.index(';')
        except ValueError:
            first_semicolon = len(body)

        # Try to find the first comma or semicolon, whichever comes first.
        if first_comma < len(body) or first_semicolon < len(body):
            if first_comma < first_semicolon:
                split = first_comma
                ty = 'AND'
            elif first_semicolon < first_comma:
                split = first_semicolon
                ty = 'OR'
        else:
            # we're done, no more tokens to much
            break
        
        head, body = body[:split], body[split+1:]
        goals.append((ty, head))

    return goals


def get_functor(term):
    functor, args = term.split('(', 1)
    args = args.split(')')[0].split(',')

    return functor, args

def get_name(functor, args):
    arity = len(args)

    return f"{functor}/{arity}"


def tokenstream(source):
    """Get the rules and facts from a source file."""
    
    sanitized = ''.join([c for c in source if c.isalpha() or c.isdigit() or c in ''.join(TOKENS)])
    
    statements = sanitized.split('.')
    rules = filter(lambda s: ':-' in s, statements)
    facts = filter(lambda s: ':-' not in s, statements)

    rule_tokens = {}
    for rule in rules:
        head, body = rule.split(':-')
        functor, args = get_functor(head)
        name = get_name(functor, args)
        
        print("HEAD", name, args)

        munched = rule_munch(body)
        print(munched)
        rule_tokens[name] = { 'args': args, 'body': munched }



    return {
        'rules': rule_tokens,
        'facts': list(facts)
    }


def main():
    parser = argparse.ArgumentParser(description="Tokenize a source file.")
    parser.add_argument('script', type=str, help="The source file to tokenize.")
    args = parser.parse_args()

    path = args.script
    name = os.path.basename(path).split('.')[0]

    source = get_source(path)
    tokened = tokenstream(source)

    yml = write_tokens(tokened, f"output/{name}.yaml")