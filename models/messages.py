from database.column import Column
from database.database import Database
from database.integer import Integer
from database.model import Model
from database.string import String
from models.users import User


class Message(Model):
    table_name: str = "messages"
    id = Column(column_type=Integer(), primary_key=True)
    user_from_id = Column(column_type=Integer(), required=True, foreign_key=Integer())
    user_to_id = Column(column_type=Integer(), required=True, foreign_key=Integer())
    text = Column(column_type=String(255), required=True)


if __name__ == "__main__":
    from settings import ROOT_DIR

    test_db = Database(db_file=f"{ROOT_DIR}/test_database.db")

    nela: User = User(username="nela", password="tests")
    if not nela.table_exists(db=test_db):
        nela.create_table(db=test_db)
    if not nela.load(db=test_db, test_exists=True, overwrite_cached=True):
        nela.save(db=test_db)
    nela.load(db=test_db)

    test_message: Message = Message(user_from_id=nela.id, user_to_id=nela.id, text="test")
    test_message.save(db=test_db)

    messages: [Message] = Message().get_instances_by_values(db=test_db, where_fields=["user_to_id"], where_values=[nela.id])
    for message in messages:
        from_user = User(id=message.user_from_id)
        from_user.load(db=test_db, overwrite_cached=True)
        from_username = from_user.username
        print(f"{from_username}: {message.text}")

    del test_db

