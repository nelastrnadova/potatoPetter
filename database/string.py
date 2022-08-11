from database.base_type import BaseType


class String(BaseType):
    def __init__(self, max_length: int = 255):
        self.max_length = max_length

    def get_sql(self) -> str:
        return f"VARCHAR({self.max_length})"
