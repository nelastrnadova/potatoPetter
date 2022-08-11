from database.column import Column


class ColumnValue:
    def __init__(self, column: Column, value: any):
        self.column: Column = column
        self.value: any = value

    def is_valid(self) -> bool:
        return self.column.column_type.is_valid(self.value)

    def get_value_as_string(self) -> str:  # TODO: prolly not the best solution?
        return self.column.column_type.get_value_as_string(self.value)
