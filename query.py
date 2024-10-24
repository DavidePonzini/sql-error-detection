import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where

import util
from sql import SQL_Code
from query_select_clauses import *
from misconceptions import Misconceptions
import schema

from dav_tools import messages



class Query(SQL_Code):
    def __init__(self, query_text: str):
        self.text = query_text
        self.queries = sqlparse.parse(self.text)

        tokens = util.merge_tokens(*self.queries)
        super().__init__(tokens)


class SelectQuery(Query):
    def __init__(self, query_text: str, schema_filepath: str):
        super().__init__(query_text)

        self.available_tables = schema.Schema(schema_filepath)

    def log_misconception(self, misconception: Misconceptions):
        messages.message(misconception.name,
                         icon=f'MISCONCEPTION {misconception.value:3}',
                         icon_options=[messages.TextFormat.Color.RED],
                         default_text_options=[messages.TextFormat.Color.RED])

    def extract_select(self) -> SelectClause:
        tokens = self._extract_clause_tokens('SELECT')
        return SelectClause(self, tokens)
    
    def extract_from(self) -> FromClause:
        tokens = self._extract_clause_tokens('FROM')
        return FromClause(self, tokens)

    def extract_where(self) -> WhereClause:
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        return WhereClause(self, tokens)
    
    def extract_group_by(self) -> GroupByClause:
        tokens = self._extract_clause_tokens('GROUP BY')
        return GroupByClause(self, tokens)
    
    def extract_having(self) -> HavingClause:
        tokens = self._extract_clause_tokens('HAVING')
        return HavingClause(self, tokens)
    
    def extract_order_by(self) -> OrderByClause:
        tokens = self._extract_clause_tokens('ORDER_BY')
        return OrderByClause(self, tokens)

    def _extract_clause_tokens(self, clause: str) -> list:
        tokens = []
        collecting = False

        for token in self.tokens:
            if (token.ttype is Keyword or token.ttype is DML) and token.value.upper() == clause:
                collecting = True
                tokens.append(token)
            elif collecting:
                if token.ttype is Keyword and token.value.upper() in ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY'] or isinstance(token, Where):
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