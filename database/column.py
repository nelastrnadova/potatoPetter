from database.base_type import BaseType


class Column:
    def __init__(self, column_type: BaseType, required: bool = False, primary_key: bool = False):
        self.column_type = column_type
        self.required = required
        self.primary_key = primary_key

    def get_sql(self) -> str:
        sql: str = f"{self.column_type.get_sql()}"
        if self.primary_key:
            sql += " PRIMARY KEY"
        if self.required:
            sql += " NOT NULL"
        return sql
