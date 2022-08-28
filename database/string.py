from database.base_type import BaseType


class String(BaseType):
    def __init__(self, max_length: int = 255):
        self.max_length = max_length

    def get_sql(self) -> str:
        return f"VARCHAR({self.max_length})"

    @staticmethod
    def is_valid(value: any) -> bool:
        return True  # TODO

    @staticmethod
    def get_value_as_string(value: any) -> str:
        return str(value)

    @staticmethod
    def get_value(value: any, skip_validation: bool = False) -> str:  # TODO: store value in here?
        if not skip_validation:
            if not String.is_valid(value):
                raise AssertionError(f"{value} not a valid string type")  # TODO: better, custom error
        return str(value)
