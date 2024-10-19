class Table:
    def __init__(self, real_name):
        self.real_name = real_name
        self.name = real_name
        self.columns = []

class Column:
    def __init__(self, real_name):
        self.real_name = real_name
        self.name = real_name
        self.is_primary_key = False
        self.is_foreign_key = False
        self.dtype = None