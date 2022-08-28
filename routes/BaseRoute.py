import json
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

    def check_params_exist(self, *args):
        missing_params: list() = list()
        for arg in args:
            if arg not in self.body:
                missing_params.append(arg)
        return missing_params

    @staticmethod
    def get_missing_params_message(missing_params: list):
        return json.dumps({"errors": "missing params", "missing_params": missing_params}), 400
