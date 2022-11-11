def pretty_facts(engine):
    for term, facts in engine.facts.items():
        for fact in facts:
            print(f'{term}({", ".join(fact)})')
    print()


def pretty_rules(engine):
    for term, rules in engine.rules.items():
        for rule in rules:
            print(rule[0], rule[1])
            print(f'{term}({", ".join(rule[0])}) :- {", ".join(rule[1])}')
    print()

def pretty_query(engine, functor, entities):
    result, results = engine.query(functor, entities)
    if result:
        print("True")
        for k, v in results.items():
            print(f"{k} = {v}")
    else:
        print("False")
    print()


def get_query():
    while True:
        query = input('query> ')
        match query:
            case 'quit':
                return None
        
        f, e = query.split('(')
        e = [x.strip() for x in e[:-1].split(',')]

        yield f, e