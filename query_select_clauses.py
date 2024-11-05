from sqlparse.tokens import Keyword
from sqlparse import tokens as ttypes

from sql import SQL_Code
import util
import schema
from misconceptions import Misconceptions

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from query import SelectQuery


class SelectQueryClause(SQL_Code):
    def __init__(self, query, tokens: list):
        super().__init__(tokens)
        self.parent: SelectQuery = query


class SelectClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.is_distinct = self.tokens[1].ttype == Keyword and self.tokens[1].value.upper() == 'DISTINCT'

        self.identifiers = util.extract_identifiers(self.tokens)
        
        self.columns = dict()
        self._load_columns()

    def _load_columns(self):
        # TODO: probably needs to be reworked: multiple columns with the same name can be projected
        available_schema = self.parent.schema_selected

        for identifier in self.identifiers:
            name = identifier.get_name()
            real_name = identifier.get_real_name()
            table_name = identifier.get_parent_name()

            column_candidates = available_schema.find_column(real_name, table_name)

            if len(column_candidates) == 0:         # no such column exists
                self.parent.log_misconception(Misconceptions.SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_COLUMN, f'{table_name}.{real_name}')

                self._add_column(name, table_name, None)
            elif len(column_candidates) == 1:       # exactly one column found
                column = column_candidates[0]

                self._add_column(name, table_name, column)
            else:                                   # too many possibile columns exist - cannot decide which one to use
                self.parent.log_misconception(Misconceptions.SYN_1_AMBIGUOUS_DATABASE_OBJECT_AMBIGUOUS_COLUMN, f'{table_name}.{real_name}')

                self._add_column(name, table_name, *column_candidates)

    def _add_column(self, column_name: str, table_name: str | None, *columns: schema.TableColumn | None):
        full_name = f'{table_name}.{column_name}'
        
        if not columns:
            return  # No columns provided; exit early
        
        # Handle adding columns dynamically
        if full_name in self.columns:
            # If current value is not a list, convert it to a list
            if not isinstance(self.columns[full_name], list):
                self.columns[full_name] = [self.columns[full_name]]
            
            # Extend the list with new columns
            self.columns[full_name].extend(columns)
        else:
            # Set as a single item if one column is provided, otherwise as a list
            self.columns[full_name] = columns[0] if len(columns) == 1 else list(columns)



class FromClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

        self.identifiers = util.extract_identifiers(self.tokens)
        self._load_tables()

        # TODO: check joins
        # TODO: subqueries and CTEs can be used in FROM clause

    def _load_tables(self):
        available_tables = self.parent.schema_full.tables

        for identifier in self.identifiers:
            name = identifier.get_name()
            real_name = identifier.get_real_name()

            if name in self.parent.schema_selected.tables:
                # multiple definitions for the same table
                self.parent.log_misconception(Misconceptions.SYN_1_AMBIGUOUS_DATABASE_OBJECT_OMITTING_CORRELATION_NAMES, name)

            if real_name in available_tables:
                self.parent.schema_selected.add_table(name, available_tables[real_name])
            else:
                self.parent.schema_selected.add_table(name, None)

                # table name does not exist
                self.parent.log_misconception(Misconceptions.SYN_2_UNDEFINED_DATABASE_OBJECT_UNDEFINED_OBJECT, real_name)

class WhereClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)

    def _check_multiple_where(self):
        clauses = self.tokens
        
        if len(clauses) == 0:
            return
        
        if len(clauses) > 2:
            # TODO: where used twice, most likely not in the right place!
            pass

        # merge multiple where clauses into a single one
        #   (if where is used twice in the 'correct' place, we have a single clause, if it is used in two random places, we have two separate clauses)

        tokens = util.merge_tokens(*clauses)

        count = 0
        for token in tokens:
            if token.ttype is ttypes.Keyword and token.value.upper() == 'WHERE':
                count += 1
        
        if count > 1:
            self.parent.log_misconception(Misconceptions.SYN_6_COMMON_SYNTAX_ERROR_USING_WHERE_TWICE)


class GroupByClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


class HavingClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


class OrderByClause(SelectQueryClause):
    def __init__(self, query, tokens: list):
        super().__init__(query, tokens)


