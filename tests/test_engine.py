from pyrology.engine.core import KnowledgeEngine


def test_query_simple():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X)."
    r = engine.query(q)

    assert (r[0] == True)


def test_query_or():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X); woman(Y); man(Y)."
    r = engine.query(q)

    assert (r[0] == True)


def test_query_and_or():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X), woman(Y); man(Y)."
    r = engine.query(q)

    assert (r[0] == True)


def test_query_unify_fail():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X), woman(X)."
    r = engine.query(q)
    assert (r[0] == False)

    q = "man(Y); woman(X), man(X)."
    r = engine.query(q)
    assert (r[0] == False)


def test_query_unify_pass():
    engine = KnowledgeEngine(path="assets/test.pl")

    q = "man(X); woman(X)."
    r = engine.query(q)
    assert (r[0] == True)
    # assert len(r[1]) == 6

    q = "man(X), woman(Y)."
    r = engine.query(q)
    assert (r[0] == True)

def test_query_sane1():
    engine = KnowledgeEngine(path="assets/test.pl")

    q1 = "man(X), woman(Y); man(Y).", True
    q2 = "man(X), woman(Y), man(Y).", False
    q3 = "man(X), woman(Y); man(Y), man(Z); woman(Z).", True

    for q, r in [q1, q2, q3]:
        result = engine.query(q)
        assert (result[0] == r)