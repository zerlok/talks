import pytest


@pytest.fixture
def your_fixture() -> str:
    return "your fixture value"


@pytest.mark.parametrize(
    ("char", "count"),  # parametrized argument names
    [
        pytest.param("e", 2, id="case 1"),
        pytest.param("u", 3, id="case 2"),
    ],
)
def test_your_name_here(
    # inject value from the fixture
    your_fixture: str,
    # inject parametrization values
    char: str,
    count: int,
) -> None:
    # assert ACTUAL == EXPECTED
    assert your_fixture.split() == ["your", "fixture", "value"]
    assert your_fixture.count(char) == count
