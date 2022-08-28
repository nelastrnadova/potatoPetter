from abc import ABC, abstractmethod


class BaseRoute(ABC):
    def __init__(self, body: dict):
        self.body: dict = body

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def post(self):
        raise NotImplementedError
