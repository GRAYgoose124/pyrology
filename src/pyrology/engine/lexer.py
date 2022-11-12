import argparse
import logging
import os

from pyrology.utils import TOKENS, attempt_take_as_binop, get_functor, get_name, get_source, write_tokens

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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
        # Grab len because it's used repeatedly.
        bodylen = len(body)
        # TODO: Is this making assumptions?
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
        # Finally, if there are no commas or semicolons, break.
        else:
            if body: # Gotta be honest, is this check necessary?
                body = attempt_take_as_binop(body)
                try:
                    functor, args = get_functor(body) 
                    name = get_name(functor, args)
                    goals.append([name, args, "FIN"]) # Super dupes!!
                # This is accounting for infix binary ops, which are not functors???
                except AttributeError:
                    goals.append([body, "FIN"])
            break
        
        # Every iteration, we're splitting t:tt, this is you're classic
        # token munching algo.
        head, body = body[:split], body[split+1:]

        # However this "lexer" works, we've decided just to try to parse every goal
        # as a binary operation at some point. 
        # 
        # I guess that works? 
        head = attempt_take_as_binop(head)
        functor, args = get_functor(head) # Duplicated?
        name = get_name(functor, args)
        goals.append([name, args, ty])

    return goals


def tokenstream(source):
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
    # Who needs whitespace? Lets just sanitize anything we're not *expecting*.
    sanitized = ''.join([c for c in source if c.isalpha() or c.isdigit() or c in ''.join(TOKENS)])
    
    # Well, I guess individual statements are separated by periods.
    #
    # This is by no means mean't to adhere to Prolog specs, rather it's
    # convenient that it does.
    statements = sanitized.split('.')
    rules = filter(lambda s: ':-' in s, statements)
    facts = list(filter(lambda s: ':-' not in s and s != '', statements))

    # Generate rule tokens.
    #
    # Let's assume that sources are well-formed, and that rules are merely
    # a sequenece of goals separated by commas and semicolons. 
    rule_tokens = {}
    for rule in rules:
        head, body = rule.split(':-')
        functor, args = get_functor(head)
        name = get_name(functor, args)
        
        goals = rule_munch(body)

        rule_tokens[name] = { 'src': rule, 'args': args, 'goals': goals }

    # Get all constants from facts.
    # We're assuming facts have NO variables.
    # git
    # Queries are effectively facts with variables, but they are handled at 
    # runtime, thus separately.
    constants = set()
    relations = {}
    for fact in facts:
        # print (fact, get_functor(fact))
        try:
            functor, args = get_functor(fact)
            name = get_name(functor, args)
        except TypeError:
            continue # Or break - phantom term is coming up.
        if name not in relations:
            relations[name] = []
        relations[name].append(args)
        constants.update(args)


    return {
        # 'variables': variables, # We don't store variables here because we perform unification 
        #                         # at runtime on local spaces.
        'constants': constants,

        'relations': relations,
        'facts': facts, # Deprecate? ALl data is in relations

        'rules': rule_tokens,
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