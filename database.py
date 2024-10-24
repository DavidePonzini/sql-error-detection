from datetime import datetime

from dav_tools import database, messages


db = database.PostgreSQL(
    database='postgres',
    host='127.0.0.1',
    user='sql_misconceptions_admin',
    password='sql'
)

schema_prefix = 'sql_misconceptions'


def setup_schema(create_tables: str) -> str:
        '''Create a unique schema with the specified tables and return its name'''
        now = datetime.now()
        schema = f'{schema_prefix}_{now.strftime("%Y%m%d%H%M%S%f")}'

        with db.connect() as c:
            c.create_schema(schema)
            # messages.info(f'Created schema "{schema}"')
            c.set_schema(schema)
            c.execute(create_tables)
            # messages.info('Created tables')
            
            c.commit()

        return schema

def delete_schema(schema: str):
    with db.connect() as c:
        c.delete_schema(schema)
        # messages.info(f'Deleted schema "{schema}"')
        
        c.commit()

def get_tables_in_schema(schema: str) -> list[tuple]:
    query = database.sql.SQL(
        '''
            SELECT
                table_name,
                table_type
            FROM
                information_schema.tables
            WHERE
                table_schema = {schema};
        ''').format(
             schema=database.sql.Placeholder('schema'),
        )

    result = db.execute_and_fetch(query, {
         'schema': schema,
    })

    return result

def get_columns_in_table(schema: str, table: str) -> list[tuple]:
    query = database.sql.SQL(
        '''
            SELECT
                c.column_name,
                c.data_type,
                -- Is Nullable as Boolean
                CASE WHEN c.is_nullable = 'YES' THEN TRUE ELSE FALSE END AS is_nullable,
                -- Primary Key as Boolean
                CASE WHEN tc_pk.constraint_type = 'PRIMARY KEY' THEN TRUE ELSE FALSE END AS is_primary_key,
                -- Unique Constraint as Boolean
                CASE WHEN tc_unique.constraint_type = 'UNIQUE' THEN TRUE ELSE FALSE END AS is_unique,
                -- Foreign Key Table and Column
                fk_info.foreign_table AS fk_table,
                fk_info.foreign_column AS fk_column
            FROM
                information_schema.columns c
                -- Primary Key
                LEFT JOIN (
                    SELECT
                        kcu.table_schema,
                        kcu.table_name,
                        kcu.column_name,
                        tc.constraint_type
                    FROM
                        information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    WHERE
                        tc.constraint_type = 'PRIMARY KEY'
                ) tc_pk ON c.table_schema = tc_pk.table_schema
                        AND c.table_name = tc_pk.table_name
                        AND c.column_name = tc_pk.column_name
                -- Unique Constraints
                LEFT JOIN (
                    SELECT
                        kcu.table_schema,
                        kcu.table_name,
                        kcu.column_name,
                        tc.constraint_type
                    FROM
                        information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    WHERE
                        tc.constraint_type = 'UNIQUE'
                ) tc_unique ON c.table_schema = tc_unique.table_schema
                        AND c.table_name = tc_unique.table_name
                        AND c.column_name = tc_unique.column_name
                -- Foreign Keys
                LEFT JOIN (
                    SELECT
                        kcu.table_schema,
                        kcu.table_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM
                        information_schema.key_column_usage kcu
                        JOIN information_schema.table_constraints tc
                        ON kcu.constraint_name = tc.constraint_name
                        AND kcu.table_schema = tc.table_schema
                        JOIN information_schema.constraint_column_usage ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    WHERE
                        tc.constraint_type = 'FOREIGN KEY'
                ) fk_info ON c.table_schema = fk_info.table_schema
                        AND c.table_name = fk_info.table_name
                        AND c.column_name = fk_info.column_name
            WHERE
                c.table_schema = {schema}
                AND c.table_name = {table}
            ORDER BY
                c.ordinal_position;

        ''').format(
            schema=database.sql.Placeholder('schema'),
            table=database.sql.Placeholder('table'),
        )

    result = db.execute_and_fetch(query, {
         'schema': schema,
         'table': table
    })

    return [{
        'column_name':      row[0],
        'data_type':        row[1],
        'is_nullable':      row[2],
        'is_primary_key':   row[3],
        'is_unique':        row[4],
        'fk_table':         row[5],
        'fk_column':        row[6],
    } for row in result]
 

    
