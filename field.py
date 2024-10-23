from abc import abstractmethod
from sqlparse import tokens as ttypes
from sqlparse import sql 
from sql import SQL_Code


class Field(SQL_Code):
    '''Base class for any value which may appear in a clause'''
    def __init__(self, tokens):
        super.__init__(tokens)

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_source_tables(self):
        pass

    @abstractmethod
    def get_return_type(self):
        pass

    @staticmethod
    def parse(identifier):
        if isinstance(identifier, sql.Identifier):
            return Column(identifier.tokens, identifier.get_real_name(), identifier.get_name(), identifier.get_parent_name())
        return Column(identifier.tokens, None, None, None)


class Column(Field):
    def __init__(self, tokens, real_name, name, parent_name):
        super.__init__(tokens)

        self.real_name = real_name
        self.name = name
        self.is_primary_key = False
        self.is_foreign_key = False
        self.parent_name = parent_name

    @staticmethod
    def parse(identifier):
        col = Column(identifier.get_real_name())
        col.name = identifier.get_name()
        col.parent = identifier.parent

        return col
    
    def get_source_tables(self):
        return self.parent
    
    def get_name(self):
        return self.name

        



class Constant(Field):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_return_type(self):
        return type(self.value)


class Operation(Field):
    def __init__(self, operator):
        super().__init__()


class BinaryOperation(Operation):
    def __init__(self, operator, value1, value2):
        super().__init__(operator)
        self.value1 = None
        self.value2 = None


class UnaryOperation(Operation):
    def __init__(self, operator, value):
        super().__init__(operator)
        self.value = None


class AggregationOperation(UnaryOperation):
    def __init__(self, operator, value):
        super().__init__(operator, value)

