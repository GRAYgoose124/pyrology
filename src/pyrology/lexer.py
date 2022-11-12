import argparse
import os

from pyrology.utils import TOKENS, attempt_take_as_binop, get_functor, get_name, get_source, write_tokens


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
        bodylen = len(body)
        first_comma = get_first_comma_not_in_parens(body) or bodylen
        try:
            first_semicolon = body.index(';')
        except ValueError:
            first_semicolon = bodylen

        # Try to find the first comma or semicolon, whichever comes first.
        if first_comma < bodylen or first_semicolon < bodylen:
            if first_comma < first_semicolon:
                split = first_comma
                ty = 'AND'
            elif first_semicolon < first_comma:
                split = first_semicolon
                ty = 'OR'
        else:
            if body:
                body = attempt_take_as_binop(body)
                goals.append([body, "FIN"])
            break
        
        head, body = body[:split], body[split+1:]

        head = attempt_take_as_binop(head)
        goals.append([head, ty])

    return goals


def tokenstream(source):
    """Get the rules and facts from a source file."""
    
    sanitized = ''.join([c for c in source if c.isalpha() or c.isdigit() or c in ''.join(TOKENS)])
    
    statements = sanitized.split('.')
    rules = filter(lambda s: ':-' in s, statements)
    facts = filter(lambda s: ':-' not in s, statements)

    # Generate rule tokens.
    rule_tokens = {}
    for rule in rules:
        head, body = rule.split(':-')
        functor, args = get_functor(head)
        name = get_name(functor, args)
        
        goals = rule_munch(body)

        rule_tokens[name] = { 'args': args, 'goals': goals }



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