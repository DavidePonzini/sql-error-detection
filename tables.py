import database

class TableColumn:
    def __init__(self, name: str, dtype: str):
        self.name: str = name
        self.dtype = dtype
        self.table = None
        self.is_primary_key: bool = False
        self.is_unique: bool = False
        self.is_nullable: bool = False
        self.foreign_key_table: str = None
        self.foreign_key_column: str = None

    @property
    def is_foreign_key(self):
        return self.foreign_key_table is not None and self.foreign_key_column is not None

    def add_to_table(self, table):
        return table.add_column(self)

    def __repr__(self):
        modifiers = ''
        if self.is_primary_key:
            modifiers += '*'
        if self.is_foreign_key:
            modifiers += '^'
        return self.name + modifiers


class Table:
    def __init__(self, name):
        self.name: str = name
        self.columns: list[TableColumn] = []

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
        return f'{self.name}({self.columns})'


def get_tables(filepath: str) -> dict[str, Table]:
    tables = {}
    
    # create the tables on a temporary schema
    schema = database.setup_schema(filepath)

    for table_name, table_type in database.get_tables_in_schema(schema):
        assert table_name not in tables, 'duplicate table'
        
        table = Table(table_name)
        tables[table_name] = table

        columns = database.get_columns_in_table(schema, table_name)
        for column in columns:
            new_col = TableColumn(column['column_name'], column['data_type'])

            new_col.is_nullable         = column['is_nullable']
            new_col.is_primary_key      = column['is_primary_key']
            new_col.is_unique           = column['is_unique']
            new_col.foreign_key_table   = column['fk_table']
            new_col.foreign_key_column  = column['fk_column']

            new_col.add_to_table(table)

    database.delete_schema(schema)

    return tables


