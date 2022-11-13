from pyrology.utils import get_functor, get_name
from pyrology.engine.lexer.utils import attempt_take_as_binop, get_first_comma_not_in_parens


def parse_rule(rule):
    head, body = rule.split(':-')
    functor, args = get_functor(head)
    name = get_name(functor, args)

    goals = rule_munch(body)

    return name, args, goals


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
            if body:  # Gotta be honest, is this check necessary?
                body = attempt_take_as_binop(body)
                try:
                    functor, args = get_functor(body)
                    name = get_name(functor, args)
                    # TODO: Should append this on '.' instead.
                    goals.append([name, args, "FIN"])  # Super dupes!!
                # This is accounting for infix binary ops, which are not functors???
                except AttributeError:
                    goals.append([body, None, "FIN"])
            break

        # Every iteration, we're splitting t:tt, this is you're classic
        # token munching algo.
        head, body = body[:split], body[split+1:]

        # However this "lexer" works, we've decided just to try to parse every goal
        # as a binary operation at some point.
        #
        # I guess that works?
        head = attempt_take_as_binop(head)
        functor, args = get_functor(head)  # Duplicated?
        name = get_name(functor, args)
        goals.append([name, args, ty])

    return goals   