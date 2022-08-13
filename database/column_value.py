from database.column import Column


class ColumnValue:
    def __init__(self, column: Column, value: any):
        self.column: Column = column
        self.value: any = value

    def is_valid(self, value: any = None) -> bool:
        if value is None:
            value = self.value
        return self.column.column_type.is_valid(value)

    def get_value_as_string(self) -> str:  # TODO: prolly not the best solution?
        return self.column.column_type.get_value_as_string(self.value)

    def set_value(self, value: any, skip_validation: bool = False):
        if not skip_validation:
            if not self.is_valid(value):
                raise ReferenceError("TODO")  # TODO: raise custom exception? more info?
        self.value = value
