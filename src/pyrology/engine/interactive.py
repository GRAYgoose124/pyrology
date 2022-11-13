import logging
from pyrology.engine.core import KnowledgeEngine
from pyrology.engine.lexer import parse_rule


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='\t| %(name)s:%(levelname)s >\t%(message)s')


class InteractiveKernel:
    def __init__(self, engine=None):
        if engine is None:
            engine = KnowledgeEngine(interactive=True)

        self.engine = engine

    def add_rule(self, rule):
        r = parse_rule(rule)
        self.engine.add_rule(*r)

    def handle_query(self, query):
        result = self.engine.query(query)
        print(result[0])

        for r in result[1]:
            for key, value in r.items():
                print(f"\t{key}: {value}")
            print()
        print()

    def cli_prompt(self):
        q = input('?- ')

        match q:
            case 'exit':
                return False
            case 'cs' | 'constants':
                print(" ".join(self.engine.constants))
            case 'rls' | 'rules':
                for name, rules in self.engine.rules.items():
                    for body in rules:
                        print(f"  {name:<15}rule: {body['src']}.")
            case 'rels' | 'relations':
                for name, args in self.engine.relations.items():
                    print(f"  {name:<10}")
                    args = [print(f"\t" + ', '.join(arg)) for arg in args]
            case 'h' | 'help':
                print('''\
                exit: exit the interactive shell
                cs: print the constants
                rls: print the rules
                rels: print the relations
                h: print this help message''')
            # Otherwise, assume it's a query.
            case _:
                if ':-' in q:
                    self.add_rule(q)
                else:
                    self.handle_query(q)

    def run(self):
        import readline

        logger.info("")
        logger.info("Welcome to Pyrology Interactive!")
        logger.info("")
        logger.info("Pyrology comes with ABSOLUTELY NO WARRANTY. This is free software.")
        logger.info("For help, please enter `?- help` for more information.")
        logger.info("")

        while True:
            try:
                self.cli_prompt()
            except EOFError:
                break
            except KeyboardInterrupt:
                print("User interrupted. Quitting...")
                break

            