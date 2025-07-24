from abc import ABC, abstractmethod
from typing import List, NamedTuple


class ParsedOrder(NamedTuple):
    external_id: str
    datetime: str
    bank: str
    amount: float
    recipient_details: str


class BaseParser(ABC):
    def __init__(self, username: str, password: str, account_name: str, telegram_id: str):
        self.username = username
        self.password = password
        self.account_name = account_name
        self.telegram_id = telegram_id

    @abstractmethod
    def login(self): ...

    @abstractmethod
    def get_new_orders(self) -> List[ParsedOrder]: ...
