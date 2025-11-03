import typing as t
from dataclasses import dataclass
from unittest.mock import ANY


@dataclass(frozen=True, kw_only=True)
class MyComplexStructure:
    attr1: str
    attr2: str
    nested_attrs: t.Sequence[str]


my_complex_structure = MyComplexStructure(attr1="attr1", attr2="attr2", nested_attrs=["nested"])
expected_value1 = "attr1"
expected_nested_count = 1

assert my_complex_structure == MyComplexStructure(
    # strict value
    attr1=expected_value1,
    # can be any value
    attr2=ANY,
    # must be a list of same length
    nested_attrs=[ANY] * expected_nested_count,
)


@dataclass(frozen=True, kw_only=True)
class UserInfo:
    id: int
    name: str
    email: str


user = UserInfo(email="john@mails.com", id=1, name="John")
users = [user]
user_ids = [1]

# good
assert user == UserInfo(
    id=1,
    name="John",
    email="john@mails.com",
    # mypy will check necessary fields and types
)
# assert always performed, order is checked too
assert [user.id for user in users] == user_ids

# bad
assert user.id == 1
assert user.name == "John"
assert user.email == "john@mails.com"
# mypy won't highlight missed field

# order is not checked, empty users ignored
for user in users:
    assert user.id in user_ids
