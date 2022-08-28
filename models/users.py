from database.column import Column
from database.database import Database
from database.integer import Integer
from database.model import Model
from database.string import String


class User(Model):
    table_name: str = "users"
    id = Column(column_type=Integer(), primary_key=True)
    username = Column(column_type=String(30), required=True, unique=True)
    password = Column(column_type=String(255), required=True)


if __name__ == "__main__":
    from settings import ROOT_DIR

    test_db = Database(db_file=f"{ROOT_DIR}/test_database.db")

    nela: User = User(username="nelala", password="meow")
    nela.username = "nela"
    beethoven: User = User(username="beethoven", password="blept")

    nela.save(db=test_db)
    nela.username = "test"
    nela.save(db=test_db)
    beethoven.save(db=test_db)

    del test_db

