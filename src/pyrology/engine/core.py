import logging
import queue
from pyrology.engine.lexer.__main__ import IgnisTokenizer
from pyrology.engine.lexer.rules import rule_munch
from pyrology.engine.lexer.utils import get_source


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

    def __init__(self, tokenizer=None, path=None, token_basis=None, interactive=False):
        if tokenizer is None:
            self.tokenizer = IgnisTokenizer()
        else:
            self.tokenizer = tokenizer

        if path is not None:
            source = get_source(path)
            token_basis = self.tokenizer.prepare(source)
        elif token_basis is None and not interactive:
            raise ValueError("No source or token basis provided.")
        elif interactive:
            self.tokenizer.prepare()

        logger.info(" - Initialized with %s constants, %s rules, and %s relations.",
                    len(self.tokenizer.constants), len(self.tokenizer.rules), len(self.tokenizer.relations))

    def _single_query(self, functor, entities):
        results = {}
        constant_matches = []
        if '/' in functor and functor.split('/')[1].isnumeric():
            term = functor
        else:
            term = f"{functor}/{len(entities)}"

        logger.debug(f"\t  Querying {term}...")
        if term not in self.tokenizer.relations:
            logger.debug(f"\t\t{term} not in facts.")
            return False, results

        for fact in self.tokenizer.relations[term]:
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
                    logger.debug("\t\t\t\tMatched %s to %s | %s",
                                e, e2, results)
                else:
                    logger.debug(
                        "\t\t\t\tFailed to match %s to %s | %s", e, e2, results)

        # checkk if all variables have been matched
        for e in entities:
            if e[0].isupper() and e not in results:
                return False, results

            # check if all constants are equal
            if e[0].islower() and e not in constant_matches:
                return False, results

        return True, results

    def _unify_bins(self, bins):
        unified = True
        final_variables = []

        for partial_results in bins:
            partial_variables = {}

            for i, (_, variables) in enumerate(partial_results):
                for key in variables:
                    for j, (_, variables2) in enumerate(partial_results):
                        if i == j:
                            continue
                        if key in variables2:
                            # TODO: This should be disable if we're ORing.
                            logger.debug("\tCross referencing %s", key)
                            if variables[key] != variables2[key]:
                                logger.debug(
                                    "  \t\"Unification\" failed: %s != %s", variables[key], variables2[key])
                                unified = False

                                if self.PASSTHROUGH_FAILURE_CONDITION:
                                    partial_variables = {
                                        key: f"Fail= !any({variables[key]} in {variables2[key]})"}
                                elif self.CLEAR_FINAL_VARIABLES_ON_FAIL:
                                    partial_variables = {}

                                break
                # Lets join all variables together for final output.
                if unified:
                    # merge variables into partial_varaibles
                    for key in variables:
                        if key not in partial_variables:
                            partial_variables[key] = set(variables[key])
                        else:
                            partial_variables[key].update(variables[key])

            final_variables.append(partial_variables)

        # TODO: Finally, we'll join all variables together.
        return unified, final_variables

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
        logger.debug('CLIQuery: %s from %s', query, input_string)

        # Check relational queries.
        final_result = None
        partial_res_sets = []
        partial_results = []

        prev_binop_comp = None
        for functor, args, binop in query:
            # check if and or
            logger.debug("  Next goal: %s(%s) %s",
                         functor, ', '.join(args), query)

            r = self._single_query(functor, args)
            logger.debug("\tPartial result: %s", r)

            if prev_binop_comp == 'OR':
                partial_res_sets.append(partial_results)
                partial_results = []
                final_result = final_result or r[0]
            elif prev_binop_comp == 'AND' or prev_binop_comp == "FIN":
                final_result = final_result and r[0]
            elif prev_binop_comp is None:
                final_result = r[0]

            logger.debug("\tFinal result: %s, %s", final_result, r[0])

            partial_results.append((r[0], r[1]))
            if binop == 'FIN':
                break

            prev_binop_comp = binop

        # Cross reference all variables used in goals. hack, TODO: unify
        # TODO: Technically we can remove final result updates prior to this point and just
        # chain here to make it.
        unify_result, final_variables = self._unify_bins(
            partial_res_sets + [partial_results])

        final_result = final_result and unify_result

        logger.debug("  Results: %s\tFinal=%s", partial_results, final_result)
        return final_result, final_variables