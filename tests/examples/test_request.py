import pytest
from _pytest.fixtures import SubRequest


def test_preview_simple_request_attrs(
    simple_request: SubRequest,
) -> None:
    with pytest.raises(AttributeError):
        assert simple_request.param

    assert simple_request.node.name.endswith(
        "test_preview_simple_request_attrs",
    )


@pytest.fixture
def simple_request(request: SubRequest) -> SubRequest:
    return request


def test_preview_params_request_attrs(
    params_request: SubRequest,
) -> None:
    left, right = params_request.param
    assert params_request.node.name.endswith(
        f"test_preview_params_request_attrs[{left} & {right}]",
    )


@pytest.fixture(
    params=[
        # NOTE: only 1 param is accepted,
        # use tuple / list / dict / dataclass
        # to pass multiple values
        pytest.param((1, 2), id="1 & 2"),
        pytest.param((3, 4), id="3 & 4"),
    ]
)
def params_request(request: SubRequest) -> SubRequest:
    return request
