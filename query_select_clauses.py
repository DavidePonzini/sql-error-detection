from sqlparse.tokens import Keyword

from sql import SQL_Code
import util


class SQL_Clause(SQL_Code):
    def __init__(self, query, tokens: list):
        super().__init__(tokens)
        self.parent = query


class SelectClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.distinct = self.tokens[1].ttype == Keyword and self.tokens[1].value.upper() == 'DISTINCT'

        self.identifiers = util.extract_identifiers(self.tokens)


class FromClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.identifiers = util.extract_identifiers(self.tokens)
        self.tables = {}        # TODO: TO BE IMPLEMENTED


class WhereClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


class GroupByClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


class HavingClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


class OrderByClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


