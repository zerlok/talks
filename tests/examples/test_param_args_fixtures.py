import pytest


def test_fixture_default_value(items: list[int]) -> None:
    assert len(items) == 42


@pytest.mark.parametrize(
    "amount",  # NOTE: also visible in fixtures!
    [pytest.param(3, id="3 items")],
)
def test_fixture_mark_parametrize(items: list[int]) -> None:
    assert len(items) == 3


@pytest.fixture()
def amount() -> int:
    return 42  # default amount


@pytest.fixture()
def items(amount: int) -> list[int]:
    return list(range(amount))
