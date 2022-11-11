class Term:
    def __init__(self, name, entities):
        self.name = name
        self.arity = len(entities)
        
        self.entities = entities
    
    def __str__(self):
        return self.__repr__()
        
    def __repr__(self):
        return f'{self.name}/{self.arity}'


