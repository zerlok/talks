# in test_my.py
import pytest


def test_my_simple_test_1() -> None:
    assert 2 + 2 == 4


def test_my_simple_test_2() -> None:
    assert 2 * 2 == 4


class TestMyGroup:
    def test_my_test_1(self) -> None:
        assert 3 + 3 == 6

    def test_my_test_2(self) -> None:
        assert 3 * 3 == 9


@pytest.fixture
def my_string() -> str:
    return "my string value!!!"


def test_my_value(
    my_string: str,  # inject value from the fixture
) -> None:
    assert my_string.split() == ["my", "string", "value!!!"]


# in test_my.py


@pytest.mark.parametrize(
    # parametrized argument names
    ("char", "count"),
    [
        pytest.param("s", 1, id="case 1"),
        pytest.param("!", 3, id="case 2"),
    ],
)
def test_my_params(
    my_string: str,  # inject value from the fixture
    char: str,
    count: int,
) -> None:
    assert my_string.count(char) == count
