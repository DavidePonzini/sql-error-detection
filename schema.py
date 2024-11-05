import database

class TableColumn:
    """
    Represents a column within a database table.

    Attributes:
        name (str): The name of the column.
        dtype (str): The data type of the column.
        table (Table | None): The table this column belongs to.
        is_primary_key (bool): Whether this column is a primary key.
        is_unique (bool): Whether this column has a unique constraint.
        is_nullable (bool): Whether this column can contain NULL values.
        foreign_key_table (str | None): The table this column references as a foreign key.
        foreign_key_column (str | None): The column in the foreign key table this column references.
    """
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
    def is_foreign_key(self) -> bool:
        """
        Checks if the column is a foreign key.

        Returns:
            bool: True if both foreign_key_table and foreign_key_column are set, False otherwise.
        """
        return self.foreign_key_table is not None and self.foreign_key_column is not None

    def add_to_table(self, table):
        """
        Adds the column to a specified table.

        Args:
            table (Table): The table to add this column to.
        
        Returns:
            TableColumn: The added column instance.
        """
        return table.add_column(self)

    def __repr__(self) -> str:
        modifiers = ''
        if self.is_primary_key:
            modifiers += '*'
        if self.is_foreign_key:
            modifiers += '^'
        return self.name + modifiers

    
class Table:
    """
    Represents a database table.

    Attributes:
        name (str): The name of the table.
        columns (list[TableColumn]): List of columns in the table.
    """
    def __init__(self, name):
        self.name: str = name
        self.columns: list[TableColumn] = []

    def add_column(self, column: TableColumn):
        """
        Adds a column to the table.

        Args:
            column (TableColumn): The column to add.

        Raises:
            AssertionError: If the column is already associated with another table.
        """
        assert column.table is None, 'Column is already associated to another table'
        column.table = self
        self.columns.append(column)

    def find_column(self, name: str) -> TableColumn | None:
        """
        Finds a column by name in the table.

        Args:
            name (str): The name of the column to find.

        Returns:
            TableColumn | None: The column if found, otherwise None.
        """
        for column in self.columns:
            if column.name == name:
                return column
        return None

    def __repr__(self) -> str:
        return f'{self.name}({self.columns})'

    def __str__(self) -> str:
        return f'{self.name}({self.columns})'

class Schema:
    """
    Represents a database schema.

    Attributes:
        text (str): The textual representation of the schema.
        db_instances (set): Set of database instance names created by this schema.
        tables (dict[str, Table]): A dictionary mapping table names to Table objects.
    """
    def __init__(self, text: str | None = None):
        self.text = text
        self.tables: dict[str, Table | None] = dict()
        
        self._db_instances = set()

        if self.text is not None:
            self.extract_tables_info_from_db()


    def __repr__(self) -> str:
        return '{' + '\n '.join(f'{k} -> {v}' for k, v in self.tables.items()) + '}'
    
    def find_column(self, column_name: str, table_name: str | None) -> list[TableColumn]:
        """
        Finds columns by name across tables or within a specified table.

        Args:
            column_name (str): The name of the column to find.
            table_name (str | None): The name of the table to search within, or None to search all tables.

        Returns:
            list[TableColumn]: List of columns matching the criteria.
        """

        # table name is known
        if table_name is not None:
            if table_name not in self.tables:
                return []
            table = self.tables[table_name]

            if table is None:   # placeholder table for undefined tables - ignore this value
                return []

            column = table.find_column(column_name)
            if column is None:
                return []
            
            return [column]

        # table name is not known
        result = []

        for table in self.tables.values():
            if table is None:   # placeholder table for undefined tables - ignore this value
                continue

            column = table.find_column(column_name)
            if column is not None:
                result.append(column)

        return result
    
    def add_table(self, name: str, table: Table | None):
        """
        Adds a table to the schema.

        Args:
            name (str): The name of the table.
            table (Table | None): The table to add to the schema.
        """
        self.tables[name] = table

    def create_instance(self) -> str:
        """
        Initializes a copy of this schema on the database.

        Returns:
            str: The name of the created schema instance.
        """

        assert self.text is not None, 'Missing creations script: cannot create this schema'

        schema = database.setup_schema(self.text)
        self._db_instances.add(schema)
        return schema

    def delete_instance(self, name: str):
        """
        Deletes a copy of this schema from the database.

        Args:
            name (str): The name of the schema instance to delete.

        Raises:
            AssertionError: If the schema instance does not exist in db_instances.
        """

        assert self.text is not None, 'Missing creations script: cannot create this schema'
        assert name in self._db_instances, 'Tried to remove a copy not created by this schema instance'
        database.delete_schema(name)
        self._db_instances.remove(name)

    def extract_tables_info_from_db(self):
        """
        Extracts tables and columns for the schema by querying the database.

        Returns:
            dict[str, Table]: Dictionary of table names to Table objects.
        """
        self.tables = dict()

        # create the tables on a temporary schema
        schema = self.create_instance()

        for table_name, table_type in database.get_tables_in_schema(schema):
            assert table_name not in self.tables, 'duplicate table'
            
            table = Table(table_name)
            self.add_table(table_name, table)

            columns = database.get_columns_in_table(schema, table_name)
            for column in columns:
                new_col = TableColumn(column['column_name'], column['data_type'])

                new_col.is_nullable         = column['is_nullable']
                new_col.is_primary_key      = column['is_primary_key']
                new_col.is_unique           = column['is_unique']
                new_col.foreign_key_table   = column['fk_table']
                new_col.foreign_key_column  = column['fk_column']

                new_col.add_to_table(table)

        self.delete_instance(schema)
