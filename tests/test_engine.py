from pyrology.engine.lib import KnowledgeEngine
from pyrology.lexer import tokenstream
from pyrology.utils import get_source


def test_engine():
    eng = KnowledgeEngine(path="assets/test.pl")

def test_engine_use():
    eng = KnowledgeEngine(path="assets/test.pl")
    
    # eng.fact('tired', ("dave",))
    # eng.fact('father', ('dave', 'joe'))
    # eng.fact('sibling', ('joe', 'jane'))
    # eng.fact('sibling', ('jane', 'joe'))

    # eng.rule('grandfather', ('X', 'Z'), [ ('father', ('X', 'Y')), 
    #                                       ('father', ('Y', 'Z')) ])
    # eng.rule('grandmother', ('X', 'Z'), [ ('mother', ('X', 'Y')), 
    #                                       ('mother', ('Y', 'Z')) ])
    
    # eng.rule('parent', ('X', 'Y'), [ ('father', ('X', 'Y')) ])

   
    # TODO:
    # eng.query
    # assert