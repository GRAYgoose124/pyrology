from pyrology.utils import get_functor, get_name
from pyrology.engine.lexer.utils import (
    get_first_comma_not_in_parens,
    get_all_delims_not_in_parens,
    BIN_TOKENS,
)


def attempt_take_as_binop(term):
    best_match = None
    for op in BIN_TOKENS:
        # if whole_op in term...
        if op in term and (
            best_match is not None
            and len(op) > len(best_match[1])
            or best_match is None
        ):
            # basically we want the regex:  f"(.*){op}(.*)"
            a, b = term.split(op, 1)
            best_match = (a, op, b)
    return best_match


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


def parse_goal(body_part):
    functor_or_binop = body_part
    maybe_binop = attempt_take_as_binop(functor_or_binop)
    if maybe_binop:
        goal = "BINOP", maybe_binop
    else:
        functor, args = get_functor(functor_or_binop)
        goal = "FUNCTOR", (functor, args)
    return goal


def rule_munch(body):
    """
    functor = name(args)
    args = [arg, arg, ...]

    rule = head :- body
    head = functor
    body = [functor<,;> functor2<,;> ...].
    """
    # strip all whitespace
    body = body.replace(" ", "")
    # We already have parsed the head, so we can just munch the body here.
    parsed_goals = []
    print(list(split_rule_goals(body)))
    for goal, delim in split_rule_goals(body):
        goal = parse_goal(goal), delim

        parsed_goals.append(goal)

    print(parsed_goals)
    return parsed_goals


def parse_rule(rule):
    head, body = rule.split(":-")
    functor, args = get_functor(head)
    name = get_name(functor, args)

    goals = rule_munch(body)

    return name, args, goals
