from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where
from enum import Enum

from sql import SQL_Code
from query import Query
import util
from misconceptions import Misconceptions

from dav_tools import messages


class SQL_Clause(Enum):
    SELECT      = 'SELECT'
    FROM        = 'FROM'
    WHERE       = 'WHERE'
    GROUP_BY    = 'GROUP BY'
    HAVING      = 'HAVING'
    ORDER_BY    = 'ORDER BY'


class SelectClause(SQL_Code):
    def __init__(self, tokens: list):
        super().__init__(tokens)

        self.distinct = self.tokens[1].ttype == Keyword and self.tokens[1].value.upper() == 'DISTINCT'

        self.identifiers = util.extract_identifiers(self.tokens)

class FromClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)

        self.identifiers = util.extract_identifiers(self.tokens)
        self.tables = None      # TODO: TO BE IMPLEMENTED


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


class SelectQuery(Query):
    def __init__(self, query_text: str):
        super().__init__(query_text)

    def log_misconception(self, misconception: Misconceptions):
        messages.message(misconception.name,
                         icon=f'MISCONCEPTION {misconception.value:3}',
                         icon_options=[messages.TextFormat.Color.RED],
                         default_text_options=[messages.TextFormat.Color.RED])

    def extract_select(self) -> SelectClause:
        tokens = self._extract_clause_tokens(SQL_Clause.SELECT)
        return SelectClause(tokens)
    
    def extract_from(self) -> FromClause:
        tokens = self._extract_clause_tokens(SQL_Clause.FROM)
        return FromClause(tokens)

    def extract_where(self) -> WhereClause:
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        return WhereClause(tokens)
    
    def extract_group_by(self) -> GroupByClause:
        tokens = self._extract_clause_tokens(SQL_Clause.GROUP_BY)
        return GroupByClause(tokens)
    
    def extract_having(self) -> HavingClause:
        tokens = self._extract_clause_tokens(SQL_Clause.HAVING)
        return HavingClause(tokens)
    
    def extract_order_by(self) -> OrderByClause:
        tokens = self._extract_clause_tokens(SQL_Clause.ORDER_BY)
        return OrderByClause(tokens)

    def _extract_clause_tokens(self, clause: SQL_Clause) -> list:
        tokens = []
        collecting = False

        for token in self.tokens:
            if (token.ttype is Keyword or token.ttype is DML) and token.value.upper() == clause.value:
                collecting = True
                tokens.append(token)
            elif collecting:
                if token.ttype is Keyword and token.value.upper() in [clause.value for clause in SQL_Clause] or isinstance(token, Where):
                    collecting = False
                    continue
                tokens.append(token)

        return tokens

    def print_tree(self):
        for q in self.queries:
            print('-' * 50)
            q._pprint_tree()
    
    def __str__(self):
        return self.text

