import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where

import util
from util import UNDEFINED
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

        self.schema = schema.Schema(schema_filepath)
        self.misconceptions = set()

        # sql clauses - order of initialization is important
        self.from_clause        = self._extract_from()
        self.where_clause       = self._extract_where()
        self.group_by_clause    = self._extract_group_by()
        self.having_clause      = self._extract_having()
        self.order_by_clause    = self._extract_order_by()
        self.select_clause      = self._extract_select()

    def log_misconception(self, misconception: Misconceptions):
        if misconception not in self.misconceptions:
            self.misconceptions.add(misconception)

    def print_misconceptions(self):
        if len(self.misconceptions) == 0:
            messages.success('No misconceptions detected')
            return
        
        for misconception in sorted(self.misconceptions, key=lambda m: m.value):
            messages.message(misconception.name,
                            icon=f'MISCONCEPTION {misconception.value:3}',
                            icon_options=[messages.TextFormat.Color.RED],
                            default_text_options=[messages.TextFormat.Color.RED])

    def _extract_select(self) -> SelectClause | None:
        tokens = self._extract_clause_tokens('SELECT')

        if len(tokens) > 0:
            return SelectClause(self, tokens)
        return None
    
    def _extract_from(self) -> FromClause | None:
        tokens = self._extract_clause_tokens('FROM')

        if len(tokens) > 0:
            return FromClause(self, tokens)
        return None

    def _extract_where(self) -> WhereClause | None:
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        if len(tokens) > 0:
            return WhereClause(self, tokens)
        return None
    
    def _extract_group_by(self) -> GroupByClause | None:
        tokens = self._extract_clause_tokens('GROUP BY')

        if len(tokens) > 0:
            return GroupByClause(self, tokens)
        return None
    
    def _extract_having(self) -> HavingClause | None:
        tokens = self._extract_clause_tokens('HAVING')

        if len(tokens) > 0:
            return HavingClause(self, tokens)
        return None
    
    def _extract_order_by(self) -> OrderByClause | None:
        tokens = self._extract_clause_tokens('ORDER BY')

        if len(tokens) > 0:
            return OrderByClause(self, tokens)
        return None

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
