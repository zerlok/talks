import typing as t
from functools import partial

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
    request: SubRequest,
    numbers: tuple[int, int],
) -> None:
    left, right = numbers
    assert request.node.name.endswith(
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
def numbers(request: SubRequest) -> tuple[int, int]:
    return request.param


class Server:
    pass


def run_fastapi_server(x: object) -> Server:
    return Server()


class TestServer(Server):
    def __init__(self, x: object) -> None:
        pass


def create_fastapi(x: object) -> object:
    return object()


def create_aiohttp(x: object) -> object:
    return object()


@pytest.fixture(params=["fastapi", "aiohttp"])
def server_runner(request: SubRequest) -> t.Callable[[], Server]:
    if request.param == "fastapi":
        return partial(run_fastapi_server, create_fastapi(...))

    elif request.param == "aiohttp":
        return partial(TestServer, create_aiohttp(...))

    else:
        msg = "unknown server kind"
        raise ValueError(msg, request.param)
