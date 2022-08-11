from abc import ABC, abstractmethod


class BaseType(ABC):
    @abstractmethod
    def get_sql(self) -> str:
        raise NotImplementedError()
