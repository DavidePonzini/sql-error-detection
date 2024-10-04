#!/usr/bin/env python

from dav_tools import argument_parser, messages, database
import os
from datetime import datetime
import collections


db = database.PostgreSQL(
    database='postgres',
    host='127.0.0.1',
    user='sql_misconceptions_admin',
    password='sql'
)

schema_prefix = 'sql_misconceptions'


def check_values(result: list[tuple], expected_result: list[tuple]):
    messages.warning('Specific values are not controlled, remember to check the query manually')

def check_row_number(result: list[tuple], expected_result: list[tuple]):
    result_rows = len(result)
    expected_result_rows = len(expected_result)

    if result_rows == expected_result_rows:
        messages.success(f'Correct amount of rows returned ({result_rows}/{expected_result_rows})')
        return True

    messages.error(f'Incorrect amount of rows returned ({result_rows}/{expected_result_rows})')
    return False


def check_columns_match(result: tuple, expected_result: tuple):
    if len(result) != len(expected_result):
        messages.error(f'Wrong number of columns returned ({len(result)}/{len(expected_result)})')
        return False
    
    result_types = [c.type_code for c in result]
    expected_result_types = [c.type_code for c in expected_result]

    if collections.Counter(result_types) == collections.Counter(expected_result_types):
        messages.success('Correct column types')
        return True
    
    messages.error('Incorrect column types')
    return True



def setup_schema(schema: str, connection: database.PostgreSQLConnection):
        connection.create_schema(schema)
        # messages.info(f'Created schema "{schema}"')
        connection.set_schema(schema)
        connection.execute(tables)
        # messages.info('Created tables')

def delete_schema(schema: str):
    with db.connect() as c:
        c.delete_schema(schema)
        # messages.info(f'Deleted schema "{schema}"')
        
        c.commit()

def check_syntax(query: str, connection: database.PostgreSQLConnection):
    try:
        connection.execute(query)
        messages.success('Query can run on empty dataset (no syntax errors)')
        
        return True
    except database._psycopg2.Error as e:
        error_type = type(e)
        messages.error('Syntax error', f'[{error_type.__name__}]', f'\n{e}',
                        text_options=[[messages.TextFormat.Style.BOLD]])
        
        return False

def check_query(tables: str, values: str, query: str, correct_query: str):
    # create a unique schema name
    now = datetime.now()
    schema = f'{schema_prefix}_{now.strftime("%Y%m%d%H%M%S%f")}'

    with db.connect() as c:
        try:
            setup_schema(schema, c)
    
            # check query for syntax errors (by running it on an empty dataset)
            if not check_syntax(query, c):
                return

            # generate test dataset
            c.execute(values)
            # messages.info('Added values')

            # get query result
            try:
                c.execute(query)
                result = c.fetch_all()
                result_columns = c._cursor.description
            except database._psycopg2.Error as e:
                error_type = type(e)
                messages.error('Syntax error in query', f'[{error_type.__name__}]', f'\n{e}',
                                text_options=[[messages.TextFormat.Style.BOLD]])
                return

            # get correct result
            try:
                c.execute(correct_query)
                correct_result = c.fetch_all()
                correct_result_columns = c._cursor.description
            except database._psycopg2.Error as e:
                error_type = type(e)
                messages.error('Syntax error in correct query!', f'[{error_type.__name__}]', f'\n{e}',
                                text_options=[[messages.TextFormat.Style.BOLD, messages.TextFormat.Style.REVERSE]])
                return

            rows_ok = check_row_number(result, correct_result)
            columns_ok = check_columns_match(result_columns, correct_result_columns)
            
            if rows_ok and columns_ok:
                check_values(result, correct_result)

        finally:
            delete_schema(schema)



if __name__ == '__main__':
    argument_parser.set_developer_info('Davide Ponzini', 'davide.ponzini@edu.unige.it')
    argument_parser.set_description('Helper tool to check query errors')
    argument_parser.add_argument('tables', help='File containing CREATE TABLE commands')
    argument_parser.add_argument('values', help='File containing INSERT INTO commands')
    argument_parser.add_argument('correct_query', help='File containing correct query to compare results to')
    argument_parser.add_argument('query', help='File(s) containing queries to check. Each file should only contain one query', nargs='+')

    with open(argument_parser.args.tables) as f:
        tables = f.read()

    with open(argument_parser.args.values) as f:
        values = f.read()

    with open(argument_parser.args.correct_query) as f:
        correct_query = f.read()

    for query_file in argument_parser.args.query: 
        messages.info('Testing file', query_file,
                      text_options=[[], [messages.TextFormat.Style.BOLD]])

        with open(query_file) as f:
            query = f.read()

        check_query(
            tables=tables,
            values=values,
            query=query,
            correct_query=correct_query
            )
        
        messages.message('=' * os.get_terminal_size().columns, default_text_options=[messages.TextFormat.Style.DIM])
        