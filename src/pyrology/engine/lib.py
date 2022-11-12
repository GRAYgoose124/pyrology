import logging
from pyrology.utils import pretty_facts, pretty_query, get_query, pretty_rules


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='\t| %(name)s:%(levelname)s >\t%(message)s')




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
    
    def rule(self, functor, entities, body):
        term = f"{functor}/{len(entities)}"

        if term not in self.rules:
            self.rules[term] = []
        self.rules[term].append((entities, body))

    def query(self, functor, entities):
        results = {}
        constant_matches = []
        term = f"{functor}/{len(entities)}"

        logger.debug(f"Querying {term}({', '.join(entities)})")
        if term not in self.facts:
            return False, results

        for fact in self.facts[term]:
            logger.debug(f"\tChecking {term}({', '.join(fact)})")

            args = list(zip(entities, fact))
            logger.debug(f"\t\tArgs: {list(args)}")
            for e, e2 in args:
                logger.debug("\t  Comparing %s to %s", e, e2)

                if e[0].isupper():
                    if e not in results:
                        results[e] = []
                    results[e].append(e2)
                elif e == e2:
                    if e not in constant_matches:
                        constant_matches.append(e)
                    logger.debug("\t\t\tMatched %s to %s | %s", e, e2, results)
                else:
                    logger.debug("\t\t\tFailed to match %s to %s | %s", e, e2, results)

        # checkk if all variables have been matched
        for e in entities:
            if e[0].isupper() and e not in results:
                return False, results
            
            # check if all constants are equal
            if e[0].islower() and e not in constant_matches:
                return False, results

        return True, results


def main():
    import readline

    eng = ScriptEngine()
    
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