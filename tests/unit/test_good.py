import pytest

from myapp.auth import SimpleAuthenticator
from myapp.user import Credentials, UserInfo

USER_CASES = pytest.mark.parametrize(
    ("username", "password"),
    [
        pytest.param("John", "secret123", id="John"),
        pytest.param("Alice", "password123", id="Alice"),
    ],
)


@USER_CASES
def test_can_authenticate_registered_user(
    auth: SimpleAuthenticator,
    registered_user: UserInfo,
    credentials: Credentials,
) -> None:
    assert auth.authenticate(credentials) == registered_user


@USER_CASES
def test_cant_authenticate_non_registered_user(
    auth: SimpleAuthenticator,
    credentials: Credentials,
) -> None:
    assert auth.authenticate(credentials) is None


@pytest.mark.parametrize("credentials_password", [pytest.param("invalid password")])
@USER_CASES
def test_cant_authenticate_registered_user_when_password_is_invalid(
    auth: SimpleAuthenticator,
    credentials: Credentials,
    password: str,  # NOTE: just for parametrize to inject `password` param arg
) -> None:
    assert auth.authenticate(credentials) is None


@pytest.fixture
def auth() -> SimpleAuthenticator:
    return SimpleAuthenticator()


@pytest.fixture
def registered_user(auth: SimpleAuthenticator, username: str, password: str) -> UserInfo:
    return auth.register(username, password)


@pytest.fixture
def credentials_username(username: str) -> str:
    return username


@pytest.fixture
def credentials_password(password: str) -> str:
    return password


@pytest.fixture
def credentials(credentials_username: str, credentials_password: str) -> Credentials:
    return Credentials(username=credentials_username, password=credentials_password)
