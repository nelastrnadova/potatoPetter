from database.base_type import BaseType


class Integer(BaseType):
    def get_sql(self) -> str:
        return f"INTEGER"

    @staticmethod
    def is_valid(value: any) -> bool:
        if isinstance(value, int):
            return True
        if isinstance(value, str):
            return value.isdigit()
        return False

    @staticmethod
    def get_value_as_string(value: any) -> str:
        return str(value)

    @staticmethod
    def get_value(value: any, skip_validation: bool = False) -> int:
        if not skip_validation:
            if not Integer.is_valid(value):
                raise AssertionError(f"{value} not a valid integer type")  # TODO: better, custom error
        return int(value)
