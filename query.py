import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where

import util
from sql import SQL_Code
from query_select_clauses import *
from misconceptions import Misconceptions
import schema

from dav_tools import messages


# Sentinel object to distinguish uninitialized state
UNDEFINED = object()


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

        # sql clauses
        self._select    = UNDEFINED
        self._from      = UNDEFINED
        self._where     = UNDEFINED
        self._group_by  = UNDEFINED
        self._having    = UNDEFINED
        self._order_by  = UNDEFINED

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

    @property
    def select_clause(self) -> SelectClause | None:
        if self._select is UNDEFINED:
            self._select = self.extract_select()

        return self._select

    @property
    def from_clause(self) -> FromClause | None:
        if self._from is UNDEFINED:
            self._from = self.extract_from()

        return self._from

    @property
    def where_clause(self) -> WhereClause | None:
        if self._where is UNDEFINED:
            self._where = self.extract_where()

        return self._where

    @property
    def group_by_clause(self) -> GroupByClause | None:
        if self._group_by is UNDEFINED:
            self._group_by = self.extract_group_by()

        return self._group_by

    @property
    def having_clause(self) -> HavingClause | None:
        if self._having is UNDEFINED:
            self._having = self.extract_having()

        return self._having

    @property
    def order_by_clause(self) -> OrderByClause | None:
        if self._order_by is UNDEFINED:
            self._order_by = self.extract_order_by()

        return self._order_by

    def extract_select(self) -> SelectClause | None:
        tokens = self._extract_clause_tokens('SELECT')

        if len(tokens) > 0:
            return SelectClause(self, tokens)
        return None
    
    def extract_from(self) -> FromClause | None:
        tokens = self._extract_clause_tokens('FROM')

        if len(tokens) > 0:
            return FromClause(self, tokens)
        return None

    def extract_where(self) -> WhereClause | None:
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        if len(tokens) > 0:
            return WhereClause(self, tokens)
        return None
    
    def extract_group_by(self) -> GroupByClause | None:
        tokens = self._extract_clause_tokens('GROUP BY')

        if len(tokens) > 0:
            return GroupByClause(self, tokens)
        return None
    
    def extract_having(self) -> HavingClause | None:
        tokens = self._extract_clause_tokens('HAVING')

        if len(tokens) > 0:
            return HavingClause(self, tokens)
        return None
    
    def extract_order_by(self) -> OrderByClause | None:
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
