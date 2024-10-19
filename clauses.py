from enum import Enum
from sqlparse.tokens import Keyword, DML

from util import strip_spaces_and_comments, _extract_identifiers



class SQL_Clause(Enum):
    SELECT      = 'SELECT'
    FROM        = 'FROM'
    WHERE       = 'WHERE'
    GROUP_BY    = 'GROUP BY'
    HAVING      = 'HAVING'
    ORDER_BY    = 'ORDER BY'


class SQL_Code:
    def __init__(self, tokens: list):
        self.tokens = strip_spaces_and_comments(tokens)

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])
    
    def __repr__(self):
        tokens = ',\n '.join([token.__repr__() for token in self.tokens])
        return f'[{tokens}]'


class SelectClause(SQL_Code):
    def __init__(self, tokens: list):
        super().__init__(tokens)

        self.distinct = self.tokens[1].ttype == Keyword and self.tokens[1].value.upper() == 'DISTINCT'

        self.identifiers = _extract_identifiers(self.tokens)


class FromClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)

        self.identifiers = _extract_identifiers(self.tokens)
        self.tables = None      # TO BE IMPLEMENTED



class WhereClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)


class GroupByClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)


class HavingClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)


class OrderByClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)