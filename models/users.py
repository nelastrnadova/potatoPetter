from database.column import Column
from database.database import Database
from database.integer import Integer
from database.model import Model
from database.string import String


class Users(Model):
    id = Column(column_type=Integer(), primary_key=True)
    username = Column(column_type=String(30), required=True)


if __name__ == "__main__":
    from settings import ROOT_DIR

    test_db = Database(db_file=f"{ROOT_DIR}/test_database.db")
    xXusrXx = Users.create_table(db=test_db)
    del test_db

