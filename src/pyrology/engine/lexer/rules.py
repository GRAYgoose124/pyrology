from pyrology.utils import get_functor, get_name
from pyrology.engine.lexer.utils import (
    attempt_take_as_binop,
    get_first_comma_not_in_parens,
    get_all_delims_not_in_parens,
)


def parse_rule(rule):
    head, body = rule.split(":-")
    functor, args = get_functor(head)
    name = get_name(functor, args)

    goals = rule_munch(body)

    return name, args, goals


def parse_goal(body_part):
    functor_or_binop = body_part
    maybe_binop = attempt_take_as_binop(functor_or_binop)
    if maybe_binop:
        goal = "BINOP", maybe_binop
    else:
        functor, args = get_functor(functor_or_binop)
        goal = "FUNCTOR", (functor, args)
    return goal


def split_rule_goals(body):
    indelims = get_all_delims_not_in_parens(body, ",;")
    start = 0
    for index, delim in indelims:
        match delim:
            case ",":
                delim = "AND"
            case ";":
                delim = "OR"

        yield body[start:index], delim
        start = index + 1

    yield body[start:], "FIN"


def rule_munch(body):
    """
    functor = name(args)
    args = [arg, arg, ...]

    rule = head :- body
    head = functor
    body = [functor<,;> functor2<,;> ...].
    """
    # strip whitespace
    body = "".join(body.split())

    # We already have parsed the head, so we can just munch the body here.
    parsed_goals = []
    print(list(split_rule_goals(body)))
    for goal, delim in split_rule_goals(body):
        goal = parse_goal(goal), delim

        parsed_goals.append(goal)

    print(parsed_goals)
    return parsed_goals
