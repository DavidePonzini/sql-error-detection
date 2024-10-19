import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where

from clauses import *





class Query(SQL_Code):
    def __init__(self, query_text: str):
        self.text = query_text
        self.query = sqlparse.parse(self.text)[0]
        super().__init__(self.query.tokens)

    def extract_select(self) -> SelectClause:
        tokens = self._extract_clause(SQL_Clause.SELECT)
        return SelectClause(tokens)
    

    def extract_from(self) -> FromClause:
        tokens = self._extract_clause(SQL_Clause.FROM)
        return FromClause(tokens)
    

    def extract_where(self) -> list:
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        return WhereClause(tokens)
    
    def extract_group_by(self) -> list:
        tokens = self._extract_clause(SQL_Clause.GROUP_BY)
        return GroupByClause(tokens)
    

    def extract_having(self) -> list:
        tokens = self._extract_clause(SQL_Clause.HAVING)
        return GroupByClause(tokens)
    

    def extract_order_by(self) -> list:
        tokens = self._extract_clause(SQL_Clause.ORDER_BY)
        return GroupByClause(tokens)
    

    def _extract_clause(self, clause: SQL_Clause) -> list:
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
        return self.query._pprint_tree()
    
    def __str__(self):
        return self.text
