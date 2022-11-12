import logging
from pyrology.utils import pretty_query


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='\t| %(name)s:%(levelname)s >\t%(message)s')


class InteractiveKernel:
    def __init__(self, engine):
        self.engine = engine

    def run(self):
        import readline

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
                case 'fs' | 'facts':
                    print(self.engine.related_facts)
                case 'cs' | 'constants':
                    print(self.engine.constants)
                case 'rls' | 'rules':
                    print(self.engine.rules)
                case 'rels' | 'relations':
                    print(self.engine.relations)
                case 'h' | 'help':
                    print('''\
                    exit: exit the interactive shell
                    fs: print the facts
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