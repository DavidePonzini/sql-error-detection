from sqlparse.tokens import Keyword

from sql import SQL_Code
import util
import schema
from misconceptions import Misconceptions


class SQL_Clause(SQL_Code):
    def __init__(self, query, tokens: list):
        super().__init__(tokens)
        self.parent = query


class SelectClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.is_distinct = self.tokens[1].ttype == Keyword and self.tokens[1].value.upper() == 'DISTINCT'

        self.identifiers = util.extract_identifiers(self.tokens)


class FromClause(SQL_Clause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.identifiers = util.extract_identifiers(self.tokens)
        self.tables = self._load_tables()

        # TODO: check joins
        # TODO: subqueries and CTEs can be used in FROM clause

    def _load_tables(self) -> dict[str, schema.Table]:
        tables = {}

        for identifier in self.identifiers:
            name = identifier.get_name()
            real_name = identifier.get_real_name()

            avaiable_tables = self.parent.schema.tables
            if name in tables:
                # multiple definitions for the same table
                self.parent.log_misconception(Misconceptions.SYN_1_AMBIGUOUS_DATABASE_OBJECT_OMITTING_CORRELATION_NAMES)

            if real_name in avaiable_tables:
                tables[name] = avaiable_tables[real_name]
            else:
                tables[name] = None

                # table name does not exist
                self.parent.log_misconception(Misconceptions.SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_OBJECT)
        
        return tables

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


