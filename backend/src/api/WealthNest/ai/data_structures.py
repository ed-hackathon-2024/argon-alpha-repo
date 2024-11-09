from typing import NamedTuple


class CategoryInformation(NamedTuple):
    name: str
    monthly_expenses: float
    currency: str
    transactions_amount: int


class StatisticalInformation(NamedTuple):
    common_transaction_name: str


class UserInformation(NamedTuple):
    goal: str
    name: str
    age: int
    gender: str
