import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import IdentifierList, Identifier, Comment, Where
from enum import Enum


def read_query(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def strip_spaces_and_comments(tokens: list) -> list:
    return [token for token in tokens if not token.is_whitespace and not isinstance(token, Comment)]


def _extract_identifiers(tokens: list):
    identifiers = []

    for token in tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                identifiers.append(identifier)
        elif isinstance(token, Identifier):
            identifiers.append(token)

    return identifiers


class SQL_Clause(Enum):
    SELECT      = 'SELECT'
    FROM        = 'FROM'
    WHERE       = 'WHERE'
    GROUP_BY    = 'GROUP BY'
    HAVING      = 'HAVING'
    ORDER_BY    = 'ORDER BY'


class SQL_Code:
    def __init__(self, tokens: list):
        self.tokens = strip_spaces_and_comments(tokens)

    def __str__(self):
        return '\n'.join([str(token) for token in self.tokens])
    
    def __repr__(self):
        tokens = ',\n '.join([token.__repr__() for token in self.tokens])
        return f'[{tokens}]'

class SelectClause(SQL_Code):
    def __init__(self, tokens: list):
        super().__init__(tokens)

        self.identifiers = _extract_identifiers(self.tokens)


class FromClause(SQL_Code):
    def __init__(self, tokens):
        super().__init__(tokens)


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


if __name__ == '__main__':
    from dav_tools import argument_parser, messages
    
    argument_parser.add_argument('file')
    text = read_query(argument_parser.args.file)
    query = Query(text)

    messages.info('============= SELECT =============')
    sel = query.extract_select()
    print(repr(sel))
    for identifier in sel.identifiers:
        messages.message(f'{identifier.get_parent_name()}.{identifier.get_real_name()} -> {identifier.get_parent_name()}.{identifier.get_name()}', icon='col', icon_options=[messages.TextFormat.Color.GREEN])

    messages.info('============= FROM =============')
    fr = query.extract_from()
    print(repr(fr))

    messages.info('============= WHERE =============')
    wh = query.extract_where()
    print(repr(wh))

    messages.info('============= GROUP BY =============')
    gb = query.extract_group_by()
    print(repr(gb))

    messages.info('============= HAVING =============')
    hav = query.extract_having()
    print(repr(hav))

    messages.info('============= ORDER BY =============')
    ob = query.extract_order_by()
    print(repr(ob))