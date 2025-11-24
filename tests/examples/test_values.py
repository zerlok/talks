import random
from datetime import date

import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture
def username(request: SubRequest) -> str:
    return f"User for {request.node.name}"


@pytest.fixture
def user_age(request: SubRequest) -> int:
    return (hash(request.node.name) % 50) + 20


@pytest.fixture(params=[20, 33, 70])
def stub_user_age(request: SubRequest) -> int:
    return request.param


# BAD: flaky tests
@pytest.fixture
def random_user_age() -> int:
    return random.randint(20, 70)


# BAD: flaky tests
@pytest.fixture(scope="session")
def user_date_of_birth() -> date:
    return date(year=2020, month=1, day=1)


@pytest.fixture
def credentials_password(request: SubRequest) -> str:
    if "password" in request.fixturenames:
        return request.getfixturevalue("password")

    return f"Password for {request.node.name}"
