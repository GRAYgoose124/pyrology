import os
import yaml


from future_algebra.tokenizer import tokenizer


class ScriptEngine:
    def __init__(self, basis=None):
        self.facts = set()
        self.rules = set()

    def parse(self, text):
        pass

    def parse_facts(self, text):
        """ Parse a string of facts into a set of facts.

        Facts are of the form:
        relation(entity, entity1).
        """
        

    def query(self, question):
        pass


def main():
    queries = ["mortal(socrates).", "human(socrates).", "man(adele)."]

    tokened = None
    with open("assets/script.futa") as f:
        # read script into a string
        script = f.read()
        tokened = tokenizer(script)

    if not os.path.exists('output'):
        os.mkdir('output')
    with open('output/tokened.yaml', 'w') as f:
        f.write(yaml.dump(tokened))
        

if __name__ == "__main__":
    main()