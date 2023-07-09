from pyrology.engine.lexer import IgnisTokenizer
from pyrology.engine.lexer.utils import (
    sanitize_src,
    get_first_comma_not_in_parens,
    get_all_delims_not_in_parens,
)
from pyrology.engine.lexer.rules import parse_rule, rule_munch, attempt_take_as_binop


import logging

logger = logging.getLogger(__name__)


class TestLexer:
    def setup_method(self):
        self.tokenizer = IgnisTokenizer()

    def test_gfcnip(self):
        s = r"siblings(X, Y) :- parent(X, Z), parent(Y, Z), X \= Y."
        idx = get_first_comma_not_in_parens(s)
        assert idx == 30

    def test_gadnip(self):
        s = r"siblings(X, Y) :- parent(X, Z), parent(Y, Z), X \= Y; notreal(X, Y)."
        idxs = get_all_delims_not_in_parens(s, ",;")
        assert [i[0] for i in idxs] == [30, 44, 52]

    def test_rm2(self):
        correct = [
            (("FUNCTOR", ("parent", ["X", "Z"])), "AND"),
            (("FUNCTOR", ("parent", ["Y", "Z"])), "AND"),
            (("BINOP", ("X", "\\=", "Y")), "OR"),
            (("FUNCTOR", ("broken", ["X", "X"])), "FIN"),
        ]
        goals = rule_munch(r" parent(X, Z), parent(Y, Z), X \= Y; broken(X, X).")
        print(goals)
        assert goals == correct, f"\ngot:\n{goals}\nexpected:\n{correct}"

    def test_parse_rule(self):
        name, args, goals = parse_rule(
            r"siblings(X, Y) :- parent(X, Z), parent(Y, Z), X \= Y."
        )
        assert name == "siblings/2"
        assert args == ["X", "Y"]
        assert goals == [
            (("FUNCTOR", ("parent", ["X", "Z"])), "AND"),
            (("FUNCTOR", ("parent", ["Y", "Z"])), "AND"),
            (("BINOP", ("X", "\\=", "Y.")), "FIN"),
        ]
