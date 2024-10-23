import util


class SQL_Code:
    def __init__(self, tokens: list):
        self.tokens = util.strip_spaces_and_comments(tokens)

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])
    
    def __repr__(self):
        tokens = ',\n '.join([token.__repr__() for token in self.tokens])
        return f'[{tokens}]'
