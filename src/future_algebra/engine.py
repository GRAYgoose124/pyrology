import logging
from future_algebra.utils import pretty_facts, pretty_query, get_query


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='\t| %(name)s:%(levelname)s >\t%(message)s')

class Term:
    def __init__(self, name, arity):
        self.name = name
        self.arity = arity
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        return f'{self.name}/{self.arity}'


class ScriptEngine:
    """
    All atoms are either constants or variables.
    All variables start with a capital letter and can be constant-substituted. (similar to type generics)
    All constants start with a lowercase letter and are unique identifiers.
    A fact is a relation with all constants.

    relation(atom, <...>).

    rule(VARIABLE, <...>) :- relation(VARIABLE, <...>)[;,] <...>.


    """
    def __init__(self, basis=None):
        self.constants = set()
        self.variables = set()

        self.rules = {}
        self.facts = {}

    def fact(self, functor, entities):
        term = f"{functor}/{len(entities)}"

        if term not in self.facts:
            self.facts[term] = []
        self.facts[term].append(entities)
        
    def query(self, functor, entities):
        results = {}
        term = f"{functor}/{len(entities)}"

        logger.debug(f"Querying {term}({', '.join(entities)})")
        if term not in self.facts:
            return False, results

        for fact in self.facts[term]:
            for e, e2 in zip(entities, fact):
                if e[0].isupper():
                    if e not in results:
                        results[e] = []
                    results[e].append(e2)
                elif e != e2:
                    return False, results
        
        return True, results


def main():
    import readline

    eng = ScriptEngine()
    
    eng.fact('tired', ("dave",))
    eng.fact('father', ('dave', 'joe'))
    eng.fact('sibling', ('joe', 'jane'))
    eng.fact('sibling', ('jane', 'joe'))

    pretty_facts(eng)
    for f, e in get_query():
        pretty_query(eng, f, e)