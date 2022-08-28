from database.base_type import BaseType


class Column:
    def __init__(self, column_type: BaseType, required: bool = False, primary_key: bool = False, unique: bool = False):
        self.column_type: BaseType = column_type
        self.required: bool = required
        self.primary_key: bool = primary_key
        self.unique: bool = True if self.primary_key else unique

    def is_primary_key(self) -> bool:  # TODO: get rid of getter? privatize self.primary_key?
        return self.primary_key

    # TODO: move sql from here to db? without making db dependant on column tho
    def get_generation_sql(self) -> str:
        sql: str = f"{self.column_type.get_sql()}"
        if self.primary_key:
            sql += " PRIMARY KEY"
        if self.required:
            sql += " NOT NULL"
        if self.unique:
            sql += " UNIQUE"
        return sql
