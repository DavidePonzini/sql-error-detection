import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Where
from typing import Any

import util
from sql import SQL_Code
from query_select_clauses import *
from misconceptions import Misconceptions
import schema

from dav_tools import messages


class Query(SQL_Code):
    """
    Represents a generic SQL query.

    Attributes:
        text (str): The text of the SQL query.
        queries (list): Parsed SQL queries from the input text.
        misconceptions (dict): Detected misconceptions.
        misconceptions (dict): Detected misconceptions.
    """
    def __init__(self, query_text: str):
        self.text = query_text
        self.queries = sqlparse.parse(self.text)
        self.misconceptions: dict[Misconceptions, Any] = dict()

        tokens = util.merge_tokens(*self.queries)
        super().__init__(tokens)

        self._check_multiple_semicolons()

    def _check_multiple_semicolons(self):
        semicolons = 0

        # we may have multiple queries if semicolon in main query
        #   or we may have a single query if semicolon in subquery

        for q in self.queries:
            for token in q.tokens:
                if token.ttype is ttypes.Punctuation and token.value == ';':
                    semicolons += 1

        if semicolons > 1:
            self.log_misconception(Misconceptions.SYN_6_COMMON_SYNTAX_ERROR_ADDITIONAL_SEMICOLON)
    
    def log_misconception(self, misconception: Misconceptions, additional_data: Any | None = None):
        """
        Logs a misconception related to the query if not already logged.

        Args:
            misconception (Misconceptions): The misconception to log.
        """
        if misconception not in self.misconceptions:
            self.misconceptions[misconception] = []

        self.misconceptions[misconception].append(additional_data)

    def print_misconceptions(self):
        """
        Prints the list of misconceptions if any are detected; otherwise, prints a success message.
        """
        if len(self.misconceptions) == 0:
            messages.success('No misconceptions detected')
            return
        
        for misconception in sorted(self.misconceptions, key=lambda m: m.value):
            messages.message(misconception.name,
                            icon=f'MISCONCEPTION {misconception.value:3}',
                            icon_options=[messages.TextFormat.Color.RED],
                            default_text_options=[messages.TextFormat.Color.RED])




class SelectQuery(Query):
    """
    Represents a SELECT SQL query with various clauses and associated schema.

    Attributes:
        schema (Schema): The database schema for the query.
        from_clause (FromClause | None): The FROM clause of the query.
        where_clause (WhereClause | None): The WHERE clause of the query.
        group_by_clause (GroupByClause | None): The GROUP BY clause of the query.
        having_clause (HavingClause | None): The HAVING clause of the query.
        order_by_clause (OrderByClause | None): The ORDER BY clause of the query.
        select_clause (SelectClause | None): The SELECT clause of the query.
    """
    def __init__(self, query_text: str, schema_filepath: str):
        super().__init__(query_text)

        self.schema_full = schema.Schema(schema_filepath)
        self.schema_selected = schema.Schema()

        # sql clauses - order of initialization is important
        self.from_clause        = self._extract_from()
        self.where_clause       = self._extract_where()
        self.group_by_clause    = self._extract_group_by()
        self.having_clause      = self._extract_having()
        self.order_by_clause    = self._extract_order_by()
        self.select_clause      = self._extract_select()

    def _extract_select(self) -> SelectClause | None:
        """
        Extracts and returns the SELECT clause from the query.

        Returns:
            SelectClause | None: The SELECT clause if found, otherwise None.
        """
        tokens = self._extract_clause_tokens('SELECT')

        if len(tokens) > 0:
            return SelectClause(self, tokens)
        return None
    
    def _extract_from(self) -> FromClause | None:
        """
        Extracts and returns the FROM clause from the query.

        Returns:
            FromClause | None: The FROM clause if found, otherwise None.
        """
        tokens = self._extract_clause_tokens('FROM')

        if len(tokens) > 0:
            return FromClause(self, tokens)
        return None

    def _extract_where(self) -> WhereClause | None:
        """
        Extracts and returns the WHERE clause from the query.

        Returns:
            WhereClause | None: The WHERE clause if found, otherwise None.
        """
        tokens = []

        for token in self.tokens:
            if isinstance(token, Where):
                tokens.append(token)

        if len(tokens) > 0:
            return WhereClause(self, tokens)
        return None
    
    def _extract_group_by(self) -> GroupByClause | None:
        """
        Extracts and returns the GROUP BY clause from the query.

        Returns:
            GroupByClause | None: The GROUP BY clause if found, otherwise None.
        """
        tokens = self._extract_clause_tokens('GROUP BY')

        if len(tokens) > 0:
            return GroupByClause(self, tokens)
        return None
    
    def _extract_having(self) -> HavingClause | None:
        """
        Extracts and returns the HAVING clause from the query.

        Returns:
            HavingClause | None: The HAVING clause if found, otherwise None.
        """
        tokens = self._extract_clause_tokens('HAVING')

        if len(tokens) > 0:
            return HavingClause(self, tokens)
        return None
    
    def _extract_order_by(self) -> OrderByClause | None:
        """
        Extracts and returns the ORDER BY clause from the query.

        Returns:
            OrderByClause | None: The ORDER BY clause if found, otherwise None.
        """
        tokens = self._extract_clause_tokens('ORDER BY')

        if len(tokens) > 0:
            return OrderByClause(self, tokens)
        return None

    def _extract_clause_tokens(self, clause: str) -> list:
        """
        Extracts tokens associated with a specific clause in the SQL query.

        Args:
            clause (str): The name of the clause (e.g., 'SELECT', 'WHERE').

        Returns:
            list: Tokens associated with the clause.
        """
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
        """
        Prints a hierarchical tree of the query structure for debugging and analysis.
        """
        for q in self.queries:
            print('-' * 50)
            q._pprint_tree()
