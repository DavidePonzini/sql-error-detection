import sqlparse
from sqlparse.tokens import Keyword, DML, DDL

import util
from sql import SQL_Code


class Query(SQL_Code):
    def __init__(self, query_text: str):
        self.text = query_text
        self.queries = sqlparse.parse(self.text)

        tokens = util.merge_tokens(*self.queries)
        super().__init__(tokens)


