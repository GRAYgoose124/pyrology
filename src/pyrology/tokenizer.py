import re

# relation(.*)
relation = re.compile(r"(\w+)\((.*)\).")
def tokenizer(text):
    """ 
    Tokenizers a string of text into a list of tokens.

    Tokens are either:
    - a variable, letters, starting with a capital
    - a constant, lowercase letters
    - a relation is a lowercase word, followed by a list of entities in parentheses
    - `(` or `)`
    - ':-' == 'if'
    - `,` == `and`
    - ';' == `or`
    - `.` == `end of statement`
    """
    relations = {}
    variables = set()
    constants = set()
    # remove all non-script characters
    text = ''.join([c for c in text if c.isalpha() or c.isdigit() or c in '(),;:-.'])
    
    stmts = text.split('.')
    tokens = []
    for stmt in stmts:
        # Rules
        if ':-' in stmt:
            head, body = stmt.split(':-')
            tokens.append((head, 'IF', tokenizer(body)))
        elif ',' in stmt:
            # get first ',' not in parentheses
            first_paren = stmt.find('(')
            last_paren = stmt.rfind(')')
            # find any commas not in parentheses
            commas = [i for i, c in enumerate(stmt) if c == ',' and i < first_paren and i > last_paren]

            for comma in commas:
                if comma < first_paren or comma > last_paren:
                    head, body = stmt.split_at(comma)
                    tokens.append((head, 'AND', tokenizer(body)))
                    break # only consuming one comma
            
        elif ';' in stmt:
            head, body = stmt.split(';', 1)
            tokens.append((head, 'OR', tokenizer(body)))
        else:
            end = None
            if '(' in stmt:
                counter = 1
                start = stmt.index('(')+1
                for i, c in enumerate(stmt[start:]):
                    if c == '(':
                        counter += 1
                    elif c == ')':
                        counter -= 1
                    if counter == 0:
                        end = i+start
                        break
                
                relation = stmt[:start-1]
                relations[relation] = {'constants': [], 'variables': []}

                entities = stmt[start:end].split(',')
                for entity in entities:
                    if entity[0].isupper():
                        relations[relation]['variables'].append(entity)
                    else:
                        relations[relation]['constants'].append(entity)

                tokens.append((relation, 'IS', entities))

    return tokens, (relations, variables, constants)
        # Fact or query, fact if all constants, query if any variables.
        