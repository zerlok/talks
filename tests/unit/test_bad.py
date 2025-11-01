from myapp.auth import SimpleAuthenticator
from myapp.user import Credentials


def test_user_authenticate() -> None:
    auth = SimpleAuthenticator()
    user = auth.register("John", "secret123")
    authenticated = auth.authenticate(Credentials(username="John", password="secret123"))
    assert authenticated.id_ == user.id_
    assert authenticated.name == "John"


def test_user_authenticate_error() -> None:
    auth = SimpleAuthenticator()
    auth.register("John", "secret123")
    authenticated = auth.authenticate(Credentials(username="John", password="invalid password"))
    assert authenticated is None
