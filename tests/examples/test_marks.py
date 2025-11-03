import pytest


@pytest.mark.xfail(reason="not implemented")
def test_fail() -> None:
    raise NotImplementedError


@pytest.mark.parametrize(
    "n",
    [
        pytest.param(42),
        pytest.param(-42, marks=[pytest.mark.skip(reason="negative")]),
    ],
)
def test_param_mark(n: int) -> None:
    assert n > 0
