import logging
from pyrology.engine.lexer import tokenstream
from pyrology.utils import get_source, pretty_facts, pretty_query, pretty_rules


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
    def __init__(self, path=None, token_basis=None, interactive=False):
        if path is not None:
            source = get_source(path)
            token_basis = tokenstream(source)
        elif token_basis is None and not interactive:
            raise ValueError("No source or token basis provided.")
        elif interactive:
            token_basis = {
                # 'variables': variables, # We don't store variables here because we perform unification 
                #                         # at runtime on local spaces.
                'constants': set(),
                'relations': {},
                'rules': {},
            }


        self.constants = token_basis['constants']
        self.rules = token_basis['rules']

        self.rels = token_basis['relations'] 
        self.relations = token_basis['relations']# token_basis['facts'] # Deprecate in facvor of relations?
        logger.debug("Engine initialized with %s constants, %s rules, %s relations, and %s facts.", len(self.constants), len(self.rules), len(self.rels), len(self.relations))
 
    def query(self, functor, entities):
        results = {}
        constant_matches = []
        term = f"{functor}/{len(entities)}"

        logger.debug(f"Querying {term}({', '.join(entities)})")
        if term not in self.relations:
            logger.debug(f"\t{term} not in facts.")
            return False, results

        for fact in self.relations[term]:
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
