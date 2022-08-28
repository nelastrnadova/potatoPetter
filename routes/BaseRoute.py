from abc import ABC, abstractmethod

from database.database import Database


class BaseRoute(ABC):
    def __init__(self, body: dict, db: Database):
        self.body: json = json.loads(body) if isinstance(body, str) else body
        self.db: Database = db

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def post(self):
        raise NotImplementedError
