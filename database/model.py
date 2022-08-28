import inspect

from database.column import Column
from database.database import Database


class Model:
    def __init__(self, **kwargs):
        self.cols: dict = dict()  # TODO: is this needed? ANSW: yes as we rewrite this later
        for col_name, col_cls in inspect.getmembers(self):
            if not isinstance(col_cls, Column):
                continue
            self.cols.update({col_name: col_cls})

        for kwarg_name in kwargs:
            setattr(self, kwarg_name, kwargs[kwarg_name])

    def create_table(self, db: Database) -> None:  # TODO: call automatically if table doesn't exist when used
        column_sqls: list[str] = list()
        for col_name, col_cls in self.cols.items():
            col_sql: str = f"'{col_name}' {col_cls.get_generation_sql()}"
            column_sqls.append(col_sql)
        db.create_table(table_name=self._get_table_name(), column_sqls=column_sqls)
        #  return True  # TODO: return if failed or not?

    def _get_table_name(self) -> str:
        if not hasattr(self, "table_name"):
            self.table_name: str = self.__name__.lower()
        return self.table_name

    def save(self, db: Database) -> int:
        if not self.table_exists(db=db):
            self.create_table(db=db)
        # TODO: check if all fields are valid and filled/non needed. if not, return or error
        if self.load(db=db, test_exists=True):
            failed: bool = self.load(db=db, overwrite_cached=False)
            #  TODO: test for failed
            pk: any = self.update(db=db)
        else:
            pk: any = self.insert(db=db)  # TODO: Union[int, str]?
        return pk

    def load(self, db: Database, test_exists: bool = False, overwrite_cached: bool = False, where_fields: [str] = None, where_values: [str] = None) -> bool:  # TODO: check for pk and load by pk first?
        table: str = self._get_table_name()
        pk: any = self.get_cached_pk_value()
        pk_col_name: str = self.get_pk_column_name()

        where_fields: [str] = list() if where_fields is None else where_fields
        where_values: [str] = list() if where_values is None else where_values

        if not where_fields:
            if not pk:
                for col_name, col_cls in self.cols.items():
                    if col_cls.unique:
                        val: any = getattr(self, col_name)
                        if isinstance(val, Column):
                            continue
                        where_fields.append(col_name)
                        where_values.append(val)
            else:
                where_fields.append(pk_col_name)
                where_values.append(pk)

        if bool(where_fields):
            data: any = db.single_select(table=table, to_select="*", where_fields=where_fields, where_values=where_values)
            if bool(data):
                if test_exists:
                    return bool(data)
                for i, col_name in enumerate(self.cols):
                    if not overwrite_cached:
                        if not isinstance(getattr(self, col_name), Column):
                            continue
                    setattr(self, col_name, data[i])
                return True
        return False

    def get_filled_columns_and_values(self):
        columns: [str] = list()
        values: [any] = list()
        for col_name, col_cls in self.cols.items():
            val: any = getattr(self, col_name)
            if isinstance(val, Column):
                continue
            columns.append(col_name)
            values.append(val)
        return columns, values

    def get_pk_column_name(self) -> str:
        for col_name, col_cls in self.cols.items():
            if col_cls.is_primary_key():  # TODO: check for multiple pks?
                return col_name
        return None  # TODO: fail?

    def get_cached_pk_value(self) -> str:  # TODO: get_pk_column_vlaue?
        pk_val: any = getattr(self, self.get_pk_column_name())
        if isinstance(pk_val, Column):
            return None
        return pk_val

    def set_cached_pk(self, pk: any) -> bool:
        for col_name, col_cls in self.cols.items():
            if col_cls.is_primary_key():  # TODO: check if multiple primary keys?
                setattr(self, col_name, pk)
                return True
        return False

    def table_exists(self, db: Database) -> bool:
        table_name: str = self._get_table_name()
        return db.table_exists(table_name)

    def insert(self, db: Database, set_pk: bool = True):
        table: str = self._get_table_name()
        columns, values = self.get_filled_columns_and_values()
        last_inserted_id: int = db.insert(table=table, columns=columns, values=values)
        if set_pk:
            setattr(self, self.get_pk_column_name(), last_inserted_id)
        return last_inserted_id

    def update(self, db: Database):  # TODO
        self.load(db=db, overwrite_cached=False)
        table: str = self._get_table_name()
        columns, values = self.get_filled_columns_and_values()
        db.update(table=table, set_fields=columns, set_values=values, where_fields=[self.get_pk_column_name()], where_values=[self.get_cached_pk_value()])
        return self.get_cached_pk_value()  # TODO: tests

    def get_instances_by_values(self, db: Database, where_fields: [str], where_values: [str]):
        raw_entries: [tuple] = db.select(table=self._get_table_name(), to_select="*", where_fields=where_fields, where_values=where_values)
        entries: list() = list()
        col_names: [str] = list(self.cols.keys())
        for raw_entry in raw_entries:
            entry = self.__class__()
            for i, col_name in enumerate(col_names):  # TODO: refactor + tests
                setattr(entry, col_name, raw_entry[i])
            entries.append(entry)
        return entries

    def get_all_instances(self, db: Database):
        raw_entries: [tuple] = db.select(table=self._get_table_name(), to_select="*")
        entries: list() = list()
        col_names: [str] = list(self.cols.keys())
        for raw_entry in raw_entries:
            entry = self.__class__()
            for i, col_name in enumerate(col_names):  # TODO: refactor + tests
                setattr(entry, col_name, raw_entry[i])
            entries.append(entry)
        return entries
