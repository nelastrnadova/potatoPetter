from database.base_type import BaseType


class Integer(BaseType):
    def get_sql(self) -> str:
        return f"INTEGER"
