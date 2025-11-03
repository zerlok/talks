from datetime import datetime, timedelta

import pytest
from _pytest.fixtures import SubRequest

from myapp.auth import ExpiredSessionError, InvalidCredentialsError, SimpleInsecureAuthenticator
from myapp.user import PasswordCredentials, SessionInfo, UserInfo
from tests.stubs.any import any_of_type
from tests.stubs.time import ManualTimeTicker

# common cases are reused
USER_CASES = pytest.mark.parametrize(
    ("username", "password"),
    [
        pytest.param("John", "secret123", id="John"),
        pytest.param("Alice", "password123", id="Alice"),
    ],
)


@USER_CASES
def test_can_register_user_with_proper_fields(
    auth: SimpleInsecureAuthenticator,
    username: str,
    password: str,
) -> None:
    assert auth.register(username, password) == UserInfo(
        id_=any_of_type(int),
        name=username,
        password=any_of_type(str),
    )


# 1) arrange via fixtures
# 2) one behavior is tested - one assert
@USER_CASES
def test_can_authenticate_registered_user(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
) -> None:
    assert auth.authenticate(credentials) == registered_user


def test_cant_authenticate_non_registered_user(
    auth: SimpleInsecureAuthenticator,
    credentials: PasswordCredentials,
) -> None:
    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(credentials)


# 1) proper naming (arrange and act are clear)
# 2) reuse `registered_user`, `credentials` fixtures, but inject incorrect password to creds
@pytest.mark.parametrize("credentials_password", [pytest.param("incorrect user password")])
@USER_CASES
def test_cant_authenticate_registered_user_with_incorrect_password(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
    password: str,  # NOTE: if not set - pytest error occurs: function uses no argument 'password'
) -> None:
    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(credentials)


@USER_CASES
def test_registered_user_can_login(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
) -> None:
    assert auth.login(credentials) == any_of_type(SessionInfo)


@pytest.mark.parametrize("ttl", [pytest.param(timedelta(hours=12))])
@USER_CASES
def test_login_session_has_appropriate_fields(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
    ticker: ManualTimeTicker,
    ttl: timedelta,
) -> None:
    assert auth.login(credentials) == SessionInfo(
        token=any_of_type(str),
        created_at=ticker(),
        expires_at=ticker() + ttl,
    )


def test_non_registered_user_cant_login(
    auth: SimpleInsecureAuthenticator,
    credentials: PasswordCredentials,
) -> None:
    with pytest.raises(InvalidCredentialsError):
        auth.login(credentials)


@pytest.mark.parametrize(
    "tick_step",
    [
        pytest.param(timedelta(), id="immediately"),
        pytest.param(timedelta(seconds=1), id="after 1 second"),
        pytest.param(timedelta(hours=1), id="after 1 hour"),
        pytest.param(timedelta(hours=11, minutes=59, seconds=59), id="1 second before expired"),
    ],
)
@USER_CASES
def test_user_can_be_authenticated_by_logged_in_session(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    logged_in_session: SessionInfo,
    tick_time: datetime,
) -> None:
    assert auth.authenticate(logged_in_session) == registered_user


@pytest.mark.parametrize(
    "tick_step",
    [
        pytest.param(timedelta(hours=12), id="on exact expire time"),
        pytest.param(timedelta(hours=12, seconds=1), id="1 second after expired"),
    ],
)
@USER_CASES
def test_logged_in_session_expires_after_ttl(
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    logged_in_session: SessionInfo,
    tick_time: datetime,
) -> None:
    with pytest.raises(ExpiredSessionError):
        auth.authenticate(logged_in_session)


@pytest.fixture
def ticker() -> ManualTimeTicker:
    # NOTE: use constant start time to make tests more reproducible
    return ManualTimeTicker(datetime(2025, 1, 1))


# NOTE: the `tick_step` fixture is not defined. Value is injected via parametrize mark.
@pytest.fixture
def tick_time(ticker: ManualTimeTicker, tick_step: timedelta) -> datetime:
    return ticker.tick(tick_step)


@pytest.fixture
def auth(ticker: ManualTimeTicker) -> SimpleInsecureAuthenticator:
    return SimpleInsecureAuthenticator(now=ticker)


# NOTE: `username` and `password` fixtures are not defined. Values are injected via parametrize mark.
@pytest.fixture
def registered_user(auth: SimpleInsecureAuthenticator, username: str, password: str) -> UserInfo:
    return auth.register(username, password)


# NOTE: build `username` for common cases (each test will use appropriate value);
# But if `username` fixture is used (e.g. via parametrize) - use that value.
@pytest.fixture
def credentials_username(request: SubRequest) -> str:
    if "username" in request.fixturenames:
        return request.getfixturevalue("username")

    return f"Username for {request.node.name}"


# NOTE: build `password` for common cases (each test will use appropriate value);
# But if `password` fixture is used (e.g. via parametrize) - use that value.
@pytest.fixture
def credentials_password(request: SubRequest) -> str:
    if "password" in request.fixturenames:
        return request.getfixturevalue("password")

    return f"Password for {request.node.name}"


@pytest.fixture
def credentials(credentials_username: str, credentials_password: str) -> PasswordCredentials:
    return PasswordCredentials(username=credentials_username, password=credentials_password)


@pytest.fixture
def logged_in_session(auth: SimpleInsecureAuthenticator, credentials: PasswordCredentials) -> SessionInfo:
    return auth.login(credentials)
