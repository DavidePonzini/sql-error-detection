from sqlparse.sql import Identifier, IdentifierList, Parenthesis
from sqlparse import tokens as ttypes

from query import Query
import util

from dav_tools import messages          # debugging


class TableColumn:
    def __init__(self, name, dtype, /,
                 is_primary_key: bool = False, is_unique: bool = False,
                 foreign_key_column = None):
        self.name = name
        self.dtype = dtype
        self.table = None
        self.is_primary_key = is_primary_key
        self.is_unique = is_unique
        self.foreign_key_column = foreign_key_column

    @property
    def is_foreign_key(self):
        return self.foreign_key_column is not None

    def __repr__(self):
        return f'|{self.name}|{"(PK)" if self.is_primary_key else ""}{"(FK)" if self.is_foreign_key else ""}{"(UQ)" if self.is_unique else ""}'


class Table:
    def __init__(self, real_name):
        self.real_name = real_name
        self.name = real_name
        self.columns = []

    def add_column(self, column: TableColumn):
        assert column.table is None, 'Column is already associated to another table'
        column.table = self
        self.columns.append(column)

    def find_column(self, name: str) -> TableColumn | None:
        for column in self.columns:
            if column.name == name:
                return column
            
        return None

    def __repr__(self):
        return f'Table <{self.name} ({self.real_name})> : {self.columns})'


class CreateQuery(Query):
    def __init__(self, query_text):
        super().__init__(query_text)

        assert self.tokens[0].ttype is ttypes.DDL

    def extract_tables(self):
        tables = []
        current_table = None

        tokens = iter(self.tokens)
        while True:
            try:
                # CREATE
                token = next(tokens)
                assert token.ttype is ttypes.DDL, f'{token} is not DDL'

                # TABLE
                token = next(tokens)
                assert token.ttype is ttypes.Keyword and token.value.upper() == 'TABLE', f'{token} is not TABLE'

                # table_name
                token = next(tokens)
                assert isinstance(token, Identifier), f'{token} is not Identifier'
                current_table = Table(token.get_name())
                tables.append(current_table)

                # columns
                token = next(tokens)
                assert isinstance(token, Parenthesis), f'{token} is not Parenthesis'

                column_tokens = iter(util.strip_spaces_and_comments(token))
                while True:
                    try:
                        collecting_column = False
                        collecting_constraint = False
                        col_token = next(column_tokens)
                        messages.info(col_token)

                        if col_token.ttype is ttypes.Punctuation and col_token.value == ',':   # comma, look for next column
                            messages.error(col_token)
                            collecting_constraint = False
                            collecting_column = False
                            continue

                        if not collecting_column and not collecting_constraint and isinstance(col_token, Identifier):
                            # Column definition or constraint
                            messages.warning(col_token)

                            # TODO: understand if it's a column or a constraint







                #             col_name = col_token.get_name()
                #             dtype_token = next(column_tokens)
                #             col_dtype = dtype_token.value

                #             # Optional column constraints
                #             is_primary_key = False
                #             is_unique = False
                #             is_foreign_key = False
                #             foreign_table = None
                #             foreign_key_column = None

                #             while True:
                #                 constraint_token = next(column_tokens)
                #                 if constraint_token.ttype is Keyword:
                #                     messages.warning(f'{current_table.name} - {constraint_token}')
                #                     if constraint_token.value.upper() == 'PRIMARY':
                #                         is_primary_key = True
                #                         # Skip "KEY"
                #                         next(column_tokens)
                #                     elif constraint_token.value.upper() == 'UNIQUE':
                #                         is_unique = True
                #                     elif constraint_token.value.upper() == 'REFERENCES':
                #                         messages.warning('ref')
                #                         is_foreign_key = True
                #                         c = next(column_tokens)
                #                         messages.warning(repr(c))
                #                         foreign_table = c.get_name()
                #                         foreign_key_column = next(column_tokens).get_name()

                #                 if constraint_token.ttype is ttypes.Punctuation and constraint_token.value == ',':
                #                     break

                #             # Add the column to the current table
                #             current_table.add_column(
                #                 TableColumn(col_name, col_dtype, current_table.name,
                #                             is_primary_key=is_primary_key,
                #                             is_unique=is_unique,
                #                             is_foreign_key=is_foreign_key,
                #                             foreign_key_name=foreign_table,
                #                             foreign_key_column=foreign_key_column)
                #             )

                #             messages.warning(f'added column {current_table.name}.{col_name}')

                    except StopIteration:
                        break  # End of columns

                # trailing semicolon
                token = next(tokens)
                assert token.ttype is ttypes.Punctuation, f'{token} is not Semicolon'

            except StopIteration:
                break

        return tables


