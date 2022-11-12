import logging
from pyrology.engine.core import KnowledgeEngine
from pyrology.utils import pretty_query, pretty_rules


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='\t| %(name)s:%(levelname)s >\t%(message)s')


class InteractiveKernel:
    def __init__(self, engine=None):
        if engine is None:
            KnowledgeEngine(interactive=True)

        self.engine = engine

    def run(self):
        import readline

        logging.info("Welcome to Pyrology! Starting interactive kernel.")
        while True:
            try:
                query = input('query> ')
            except EOFError:
                break
            except KeyboardInterrupt:
                print("User interrupted. Quitting...")
                break

            match query:
                case 'exit':
                    break
                case 'cs' | 'constants':
                    print(self.engine.constants)
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
                case _:
                    try:
                        f, e = query.split('(')
                        e = [x.strip() for x in e.split(')')[0].split(',')]
                    except ValueError:
                        print("Invalid query, try again.")
                        continue
                    
                    logger.debug("Query: %s = (%s, %s)", query, f, e)
                    pretty_query(self.engine, f, e)