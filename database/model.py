from database.column import Column
from database.database import Database


class Model:
    @classmethod
    def __init__(cls, **kwargs):
        for arg in kwargs:
            col: Column = getattr(cls, arg)
            col.set_value(kwargs[arg])

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

    @classmethod
    def save(cls, db: Database) -> int:
        if not cls.table_exists(db=db):
            cls.create_table(db=db)
        # TODO: select from db
        # TODO: if not exists insert
        return cls.insert(db=db)
        # TODO: if exists
        # TODO: cls.update(cls, db=db)

    @classmethod
    def table_exists(cls, db: Database) -> bool:
        table_name: str = cls._get_table_name()
        return db.table_exists(table_name)

    @classmethod
    def insert(cls, db: Database):
        sql: str = cls._generate_sql_insert()
        db.exec(sql)
        db.commit()
        cls.id = db.get_last_id()   # TODO: load id by primary_key?
        return cls.id

    @classmethod
    def _generate_sql_insert(cls) -> str:
        sql: str = ""
        table_name = cls._get_table_name()

        columns: dict = dict()
        for col_name, col_cls in cls.__dict__.items():
            if not isinstance(col_cls, Column):
                continue
            if col_cls.has_been_set:
                columns.update({col_name: f"'{col_cls.get_value_as_string()}'"})  # TODO: sqllite limited

        sql += f"INSERT INTO {table_name} ("

        sql += ", ".join(list(columns.keys()))

        sql += ")"
        sql += " VALUES ("

        sql += ", ".join(list(columns.values()))

        sql += ");"

        return sql
