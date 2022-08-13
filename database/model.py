import inspect

from database.column import Column
from database.column_value import ColumnValue
from database.database import Database


class Model:
    def __init__(self, **kwargs):
        self.cols: dict = dict()
        for col_name, col_cls in inspect.getmembers(self):
            if not isinstance(col_cls, Column):
                continue
            self.cols.update({col_name: col_cls})
            setattr(self, col_name, None)  # TODO: none? mb just del?
            if col_name not in kwargs:
                continue
            col_value = kwargs[col_name]
            setattr(self, col_name, ColumnValue(col_cls, col_value))

    @classmethod
    def create_table(cls, db: Database):  # TODO: call automatically if table doesn't exist when used
        sql: str = cls._generate_sql_create_table()
        db.exec(sql)

    @classmethod
    def _get_table_name(cls) -> str:
        try:
            table_name: str = cls.table_name
        except AttributeError:  # TODO: is try catch the best solution?
            table_name: str = cls.__name__.lower()
        return table_name

    @classmethod
    def _generate_sql_create_table(cls) -> str:
        sql: str = ""

        table_name = cls._get_table_name()

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

    def save(self, db: Database) -> int:
        if not self.table_exists(db=db):
            self.create_table(db=db)
        # TODO: select from db
        # TODO: if not exists insert
        return self.insert(db=db)  # TODO: set pk
        # TODO: if exists
        # TODO: cls.update(cls, db=db)

    @classmethod
    def table_exists(cls, db: Database) -> bool:
        table_name: str = cls._get_table_name()
        return db.table_exists(table_name)

    def insert(self, db: Database):
        sql: str = self._generate_sql_insert()
        db.exec(sql)
        db.commit()
        # TODO: set PK
        return db.get_last_id()

    def _generate_sql_insert(self) -> str:
        sql: str = ""
        table_name = self._get_table_name()

        columns: dict = dict()
        for col_name, col_cls in inspect.getmembers(self):
            if not isinstance(col_cls, ColumnValue):
                continue
            columns.update({col_name: f"'{col_cls.get_value_as_string()}'"})  # TODO: sqllite limited

        sql += f"INSERT INTO {table_name} ("

        sql += ", ".join(list(columns.keys()))

        sql += ")"
        sql += " VALUES ("

        sql += ", ".join(list(columns.values()))

        sql += ");"

        return sql
