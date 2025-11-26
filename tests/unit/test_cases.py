from dataclasses import dataclass, field
from datetime import datetime, timedelta

import pytest
from pytest_case_provider import CaseContainer

from myapp.auth import ExpiredSessionError, InvalidCredentialsError, SimpleInsecureAuthenticator
from myapp.user import PasswordCredentials, SessionInfo, UserInfo
from tests.mimic.any import of_type
from tests.mimic.time import ManualTimeTicker


@dataclass(frozen=True)
class UserCase:
    username: str
    password: str = field(repr=False)


CASES = CaseContainer[UserCase]()


@CASES.inject_func()
def test_can_register_user_with_proper_fields(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
) -> None:
    assert auth.register(case.username, case.password) == UserInfo(
        id_=of_type(int),
        name=case.username,
        password=of_type(str),
    )


# 1) arrange via fixtures
# 2) one behavior is tested - one assert
@CASES.inject_func()
def test_can_authenticate_registered_user(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
) -> None:
    assert auth.authenticate(credentials) == registered_user


@CASES.inject_func()
def test_cant_authenticate_non_registered_user(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
    credentials: PasswordCredentials,
) -> None:
    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(credentials)


# 1) proper naming (arrange and act are clear)
# 2) reuse `registered_user`, `credentials` fixtures, but inject incorrect password to creds
@pytest.mark.parametrize("credentials_password", [pytest.param("incorrect user password")])
@CASES.inject_func()
def test_cant_authenticate_registered_user_with_incorrect_password(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
) -> None:
    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(credentials)


@pytest.mark.parametrize("ttl", [pytest.param(timedelta(hours=12))])
@CASES.inject_func()
def test_login_session_has_proper_fields(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    credentials: PasswordCredentials,
    ticker: ManualTimeTicker,
    ttl: timedelta,
) -> None:
    assert auth.login(credentials) == SessionInfo(
        token=of_type(str),
        created_at=ticker(),
        expires_at=ticker() + ttl,
    )


@CASES.inject_func()
def test_non_registered_user_cant_login(
    case: UserCase,
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
@CASES.inject_func()
def test_user_can_be_authenticated_by_logged_in_session(
    case: UserCase,
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
@CASES.inject_func()
def test_logged_in_session_expires_after_ttl(
    case: UserCase,
    auth: SimpleInsecureAuthenticator,
    registered_user: UserInfo,
    logged_in_session: SessionInfo,
    tick_time: datetime,
) -> None:
    with pytest.raises(ExpiredSessionError):
        auth.authenticate(logged_in_session)


@CASES.case()
def john_case() -> UserCase:
    return UserCase("John", "secret123")


@CASES.case()
def alice_case() -> UserCase:
    return UserCase("Alice", "password123")


@pytest.fixture
def ticker() -> ManualTimeTicker:
    # NOTE: use constant start time to make tests reproducible
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
def registered_user(auth: SimpleInsecureAuthenticator, case: UserCase) -> UserInfo:
    return auth.register(case.username, case.password)


@pytest.fixture
def credentials_username(case: UserCase) -> str:
    return case.username


@pytest.fixture
def credentials_password(case: UserCase) -> str:
    return case.password


@pytest.fixture
def credentials(credentials_username: str, credentials_password: str) -> PasswordCredentials:
    return PasswordCredentials(username=credentials_username, password=credentials_password)


@pytest.fixture
def logged_in_session(auth: SimpleInsecureAuthenticator, credentials: PasswordCredentials) -> SessionInfo:
    return auth.login(credentials)
