import logging
from pyrology.utils import pretty_facts, pretty_query, get_query, pretty_rules


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='\t| %(name)s:%(levelname)s >\t%(message)s')


class KnowledgeEngine:
    """
    Nos - 
    - All atoms are either constants or variables.
    - All variables start with a capital letter and can be constant-substituted. (similar to type generics)
    - All constants start with a lowercase letter and are unique identifiers.
    - A fact is a relation with all constants.
    - Unification is the process of finding a substitution that makes two terms 
    equal.



    Runtime !~!TODO!~!
    In the unification stage, we'll attempt to unify each Var token
    with a constant token, and if that fails, we'll attempt to unify
    it with another Var token. If that fails, we'll just leave it as
    a Var token. 

    If we cannot unify all Var tokens with constants, the goals cannot
    be satisfied, and we'll throw an error.
    """
    def __init__(self, basis):
        # I believe we don't need to save a set of variables at this level.
        self.variables = set()

        self.constants = basis['constants']
        self.rules = basis['rules']
        self.relations = basis['relations'] 

        self.facts = basis['facts'] # Deprecate in facvor of relations?

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
