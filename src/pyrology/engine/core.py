import logging
import queue
from pyrology.engine.lexer import rule_munch, tokenstream
from pyrology.utils import get_source


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class KnowledgeEngine:
    CLEAR_FINAL_VARIABLES_ON_FAIL = False
    PASSTHROUGH_FAILURE_CONDITION = True
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

        self.relations = token_basis['relations']# token_basis['facts'] # Deprecate in facvor of relations?
        logger.info("Engine initialized with %s constants, %s rules, and %s relations/facts.", len(self.constants), len(self.rules), len(self.relations))
 
    def query(self, input_string):
        # Basic query of the form:
        # functor(arg1, arg2, ...)[,; functor2(arg1, arg2, ...) [,; ...]].
        #
        # We'll perform all queries separately, then chain their result,
        # ANDING or ORING them together based on the separator used.
        #
        # TODO: shortcircuit optimization
        input_string = input_string.replace(" ", "")

        query = rule_munch(input_string)
        logger.debug('CLIQuery: %s from %s', query , input_string)
        
        # Check relational queries.
        final_result = True
        partial_results = []

        next_binop_comp = None
        for functor, args, binop in query:
            # check if and or 
            logger.debug("  Next goal: %s(%s) %s", functor, ', '.join(args), query)

            r = self.functor_query(functor, args)
            logger.debug("\tPartial result: %s", r)

            partial_results.append((r[0], r[1], next_binop_comp))
            if binop == 'FIN':
                break

            next_binop_comp = binop
    
        # Cross reference all variables used in goals. hack, TODO: unify
        final_variables = {}
        # TODO: Technically we can remove final result updates prior to this point and just
        # chain here to make it.
        for i, (result, variables, _) in enumerate(partial_results):
            for key in variables:
                for j, (result2, variables2, compose_op) in enumerate(partial_results):
                    if i == j:
                        continue
                    if key in variables2:
                        if compose_op == 'AND' or compose_op == "FIN":
                            r = result and result2
                        elif compose_op == 'OR':
                            r = result or result2
                        final_result = final_result and r

                        if compose_op == 'OR' and r or compose_op == None:
                            break

                        # TODO: This should be disable if we're ORing.
                        logging.debug("\tCross referencing", key, variables[key], variables2[key])
                        if variables[key] != variables2[key]:
                            logger.debug("  \t\"Unification\" failed: %s != %s, OR: %s", variables[key], variables2[key], compose_op)
                            final_result = False
                      
                            if self.PASSTHROUGH_FAILURE_CONDITION:  
                                final_variables = {key: f"Fail= !any({variables[key]} in {variables2[key]})"}
                            elif self.CLEAR_FINAL_VARIABLES_ON_FAIL:
                                final_variables = {}

                            break
            # Lets join all variables together for final output.
            if final_result:
                # merge variables into final_variables
                for key in variables:
                    if key not in final_variables:
                        final_variables[key] = set(variables[key])
                    else:
                        final_variables[key].update(variables[key])

        logger.debug("  Results: %s\tFinal=%s", partial_results, final_result)
        return final_result, final_variables


    def functor_query(self, functor, entities):
        results = {}
        constant_matches = []
        if '/' in functor and functor.split('/')[1].isnumeric():
            term = functor
        else:
            term = f"{functor}/{len(entities)}"

        logger.debug(f"\t  Querying {term}...")
        if term not in self.relations:
            logger.debug(f"\t\t{term} not in facts.")
            return False, results

        for fact in self.relations[term]:
            logger.debug(f"\tChecking {term}({', '.join(fact)})")

            args = list(zip(entities, fact))
            logger.debug(f"\t\t  Args: {list(args)}")
            for e, e2 in args:
                logger.debug("\t\t\t Comparing %s to %s", e, e2)

                if e[0].isupper():
                    if e not in results:
                        results[e] = []
                    results[e].append(e2)
                elif e == e2:
                    if e not in constant_matches:
                        constant_matches.append(e)
                    logger.debug("\t\t\t\tMatched %s to %s | %s", e, e2, results)
                else:
                    logger.debug("\t\t\t\tFailed to match %s to %s | %s", e, e2, results)

        # checkk if all variables have been matched
        for e in entities:
            if e[0].isupper() and e not in results:
                return False, results
            
            # check if all constants are equal
            if e[0].islower() and e not in constant_matches:
                return False, results

        return True, results
