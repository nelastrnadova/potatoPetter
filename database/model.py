from database import database
from database.column import Column


class Model:
    @classmethod
    def create_table(cls, db: database):
        sql = cls.generate_sql()
        db.exec(sql)

    @classmethod
    def generate_sql(cls) -> str:
        sql: str = ""

        table_name: str = cls.__name__
        sql += f"CREATE TABLE {table_name} ("

        columns: list[str] = list()
        for col_name, col_cls in cls.__dict__.items():
            if not isinstance(col_cls, Column):
                continue
            col_sql = f"{col_name} {col_cls.get_sql()}"
            columns.append(col_sql)
        sql += "\n,".join(columns)

        sql += ");"

        return sql
