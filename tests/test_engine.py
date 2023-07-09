from pyrology.engine.core import KnowledgeEngine


class TestEngine:
    def setup_method(self, method):
        self.engine = KnowledgeEngine(path="assets/test.pl")

    def test_query_simple(self):
        q = "man(X)."
        r = self.engine.query(q)

        assert r[0] == True

    def test_query_or(self):
        q = "man(X); woman(Y); man(Y)."
        r = self.engine.query(q)

        assert r[0] == True

    def test_query_and(self):
        q = "man(X), woman(Y)."
        r = self.engine.query(q)

        assert r[0] == True

        q = "man(X), woman(X)."
        r = self.engine.query(q)

        assert r[0] == False

    def test_query_and_or(self):
        q = "man(X), woman(Y); man(Y)."
        r = self.engine.query(q)

        assert r[0] == True

        q = "man(X), woman(X); man(Y)."
        r = self.engine.query(q)

        assert r[0] == False

    def test_query_unify_fail(self):
        q = "man(X), woman(X)."
        r = self.engine.query(q)
        assert r[0] == False

        q = "man(Y); woman(X), man(X)."
        r = self.engine.query(q)
        assert r[0] == False

    def test_query_unify_pass(self):
        q = "man(X); woman(X)."
        r = self.engine.query(q)
        assert r[0] == True
        # assert len(r[1]) == 6

        q = "man(X), woman(Y)."
        r = self.engine.query(q)
        assert r[0] == True

    def test_query_sane1(self):
        queries = [
            ("man(X), woman(Y); man(Y).", True),
            ("man(X), woman(Y), man(Y).", False),
            ("man(X), woman(Y); man(Y), man(Z); woman(Z).", True),
            # test knowledge base
            ("man(aristotle).", True),
            ("human(aristotle).", True),
            ("mortal(aristotle).", True),
            ("mammal(aristotle).", True),
            ("animal(aristotle).", True),
            ("child(aristotle, john).", False),
            ("child(bertha, adele).", True),
        ]

        for q, r in queries:
            result = self.engine.query(q)
            assert result[0] == r, f"Query: {q}"


if __name__ == "__main__":
    import pytest

    pytest.main()
