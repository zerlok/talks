from datetime import UTC, datetime, timedelta

import pytest
from _pytest.monkeypatch import MonkeyPatch

from myapp.auth import ExpiredSessionError, InvalidCredentialsError, SimpleInsecureAuthenticator
from myapp.user import PasswordCredentials, TokenCredentials


# 1) unclear test name (what is expected?)
# 2) unclear arrange & act
# 3) partial fields check
# 4) constants in test
def test_user_authenticate() -> None:
    auth = SimpleInsecureAuthenticator()
    user = auth.register("John", "secret123")
    authenticated = auth.authenticate(PasswordCredentials(username="John", password="secret123"))
    assert authenticated.id_ == user.id_
    assert authenticated.name == "John"


# 1) unclear test name (what was arranged to cause the error?)
# 2) unclear arrange & act
# 3) multiple cases grouped (invalid password, non-registered user)
# 4) constants in test
def test_user_authenticate_error() -> None:
    auth = SimpleInsecureAuthenticator()
    auth.register("John", "secret123")
    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(PasswordCredentials(username="John", password="invalid password"))

    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(PasswordCredentials(username="does not exist", password="does not exist"))


# 1) unclear test name (what is expected?)
# 2) arrange -> act -> assert flow is broken
# 3) constants in test
# 4) partial fields check
def test_user_login() -> None:
    auth = SimpleInsecureAuthenticator()
    user1 = auth.register("John", "secret123")
    session = auth.login(PasswordCredentials(username="John", password="secret123"))
    assert session.token

    user2 = auth.authenticate(TokenCredentials(token=session.token))
    assert user2.id_ == user1.id_
    assert user2.name == "John"


# 1) unclear test name (what was arranged to cause the error?)
# 2) unclear arrange & act
# 3) constants in test
def test_user_login_error() -> None:
    auth = SimpleInsecureAuthenticator()
    auth.register("John", "secret123")
    auth.login(PasswordCredentials(username="John", password="secret123"))

    with pytest.raises(InvalidCredentialsError):
        auth.authenticate(TokenCredentials(token="invalid token"))


# 1) unclear test name (what was arranged and what is expected?)
# 2) unclear arrange & act
# 3) not a block box testing (monkeypatching)
# 3) constants in test
def test_user_login_ttl(monkeypatch: MonkeyPatch) -> None:
    auth = SimpleInsecureAuthenticator()
    auth.register("John", "secret123")
    session = auth.login(PasswordCredentials(username="John", password="secret123"))

    now = datetime.now(UTC)
    monkeypatch.setattr(auth, "_SimpleInsecureAuthenticator__now", lambda: now + timedelta(hours=12))

    with pytest.raises(ExpiredSessionError):
        auth.authenticate(session)
