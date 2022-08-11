from database.base_type import BaseType


class Column:
    def __init__(self, column_type: BaseType, value: any = None, required: bool = False, primary_key: bool = False, has_been_set: bool = False):
        self.column_type: BaseType = column_type
        self.value: any = value
        self.required: bool = required
        self.primary_key: bool = primary_key
        self.has_been_set: bool = has_been_set

    def get_sql(self) -> str:
        sql: str = f"{self.column_type.get_sql()}"
        if self.primary_key:
            sql += " PRIMARY KEY"
        if self.required:
            sql += " NOT NULL"
        return sql

    def is_valid(self) -> bool:
        return self.column_type.is_valid(self.value)

    def set_value(self, value: any):
        self.value = value
        self.has_been_set = True

    def get_value_as_string(self) -> str:  # TODO: prolly not the best solution?
        return self.column_type.get_value_as_string(self.value)
