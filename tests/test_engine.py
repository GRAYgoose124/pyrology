from pyrology.engine.lib import KnowledgeEngine
from pyrology.utils import pretty_facts, pretty_query, get_query, pretty_rules


def test_engine():
    engine = KnowledgeEngine()

def test_engine_use():
    import readline

    eng = KnowledgeEngine()
    
    eng.fact('tired', ("dave",))
    eng.fact('father', ('dave', 'joe'))
    eng.fact('sibling', ('joe', 'jane'))
    eng.fact('sibling', ('jane', 'joe'))

    eng.rule('grandfather', ('X', 'Z'), [ ('father', ('X', 'Y')), 
                                          ('father', ('Y', 'Z')) ])
    eng.rule('grandmother', ('X', 'Z'), [ ('mother', ('X', 'Y')), 
                                          ('mother', ('Y', 'Z')) ])
    
    eng.rule('parent', ('X', 'Y'), [ ('father', ('X', 'Y')) ])

    print(eng.rules)
    pretty_facts(eng)
    pretty_rules(eng)
    for f, e in get_query():
        pretty_query(eng, f, e)