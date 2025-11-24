import typing as t
from sqlite3 import Connection

import pytest
from _pytest.fixtures import SubRequest


def test_setup_teardown(setup_teardown_value: str) -> None:
    assert setup_teardown_value == "setup_teardown_value"
    # raise RuntimeError("boom")


@pytest.fixture
def setup_teardown_value(request: SubRequest) -> t.Iterator[str]:
    print("setup")
    yield "setup_teardown_value"
    print("teardown")


class UserRepository:
    def __init__(self, conn: Connection) -> None:
        pass


async def cleanup_tables(conn: Connection) -> None:
    pass


@pytest.fixture()
def connection() -> Connection: ...


@pytest.fixture
async def user_repository(connection: Connection) -> UserRepository:
    await cleanup_tables(connection)
    return UserRepository(connection)
