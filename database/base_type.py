from abc import ABC, abstractmethod


class BaseType(ABC):
    @abstractmethod
    def get_sql(self) -> str:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def is_valid(value: any) -> bool:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def get_value_as_string(value: any) -> bool:
        raise NotImplementedError()
