import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import IdentifierList, Identifier, Comment
from enum import Enum


def read_query(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def strip_spaces_and_comments(tokens: list) -> list:
    return [token for token in tokens if not token.is_whitespace and not isinstance(token, Comment)]




def _extract_identifiers(tokens: list):
    identifiers = []

    for token in tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                identifiers.append(identifier)
        elif isinstance(token, Identifier):
            identifiers.append(token)

    return identifiers


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
    

class SelectClause(SQL_Code):
    def __init__(self, tokens: list):
        super().__init__(tokens)

        self.identifiers = _extract_identifiers(self.tokens)


class FromClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)


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


class Query(SQL_Code):
    def __init__(self, query_text: str):
        text = sqlparse.parse(query_text)[0]
        self.text = text
        super().__init__(self.text.tokens)

    @property
    def select(self) -> SelectClause:
        tokens = self._extract_clause(SQL_Clause.SELECT)
        return SelectClause(tokens)
    
    def _extract_clause(self, clause: SQL_Clause) -> list:
        clause_tokens = []
        collecting = False

        for token in self.tokens:
            if (token.ttype is Keyword or token.ttype is DML) and token.value.upper() == clause.value:
                collecting = True
                clause_tokens.append(token)
            elif collecting:
                if token.ttype is Keyword and token.value.upper() not in [clause.value, ',']:
                    break
                clause_tokens.append(token)

        return clause_tokens

