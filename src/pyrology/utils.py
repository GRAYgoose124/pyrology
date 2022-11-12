import os
import yaml
# Lexer utils
BIN_TOKENS = [f"\\{op}" for op in ['=', '+', '-', '*']]
TOKENS = ['(', ')', ',', ';', ':-', '.'] + BIN_TOKENS


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


def attempt_take_as_binop(term):
    if "\\" in term:
        for op in BIN_TOKENS:
            if op in term:
                a, b = term.split(op)
                return [a, op, b]
    else:
        return term

def get_functor(term):
    try:
       functor, args = term.split('(', 1)
    except ValueError as e:
        print(f"Invalid term: {term}")
        return None 
        
    args = args.split(')')[0].split(',')
    print(term, '->', f"functor={functor}, args={args}")

    return functor, args

def get_name(functor, args):
    arity = len(args)

    return f"{functor}/{arity}"


# Output
def pretty_facts(engine):
    for term, facts in engine.facts.items():
        for fact in facts:
            print(f'{term}({", ".join(fact)})')
    print()

def pretty_rules(engine):
    for term, rules in engine.rules.items():
        for rule in rules:
            print(rule[0], rule[1])
            print(f'{term}({", ".join(rule[0])}) :- {", ".join(rule[1])}')
    print()

def pretty_query(engine, functor, entities):
    result, results = engine.query(functor, entities)
    if result:
        print("True")
        for k, v in results.items():
            print(f"{k} = {v}")
    else:
        print("False")
    print()


def get_query():
    while True:
        query = input('query> ')
        match query:
            case 'quit':
                return None
        
        f, e = query.split('(')
        e = [x.strip() for x in e[:-1].split(',')]

        yield f, e