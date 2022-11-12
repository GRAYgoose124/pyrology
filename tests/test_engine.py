from pyrology.engine.core import KnowledgeEngine
from pyrology.engine.lexer import tokenstream
from pyrology.utils import get_source


def test_query_simple():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X)."
    r = engine.query(q)

    assert(r[0] == True)

def test_query_or():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X); woman(Y); man(Y)."
    r = engine.query(q)

    assert(r[0] == True)

def test_query_and_or():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X), woman(Y); man(Y)."
    r = engine.query(q)

    assert(r[0] == True)

def test_query_unify_fail():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X), woman(X)."
    r = engine.query(q)
    assert(r[0] == False)

    q = "man(Y); woman(X), man(X)."
    r = engine.query(q)
    assert(r[0] == False)


def test_query_unify_pass():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X); woman(X)."
    r = engine.query(q)
    assert(r[0] == True)

    q = "man(X), woman(Y)."
    r = engine.query(q)
    assert(r[0] == True)