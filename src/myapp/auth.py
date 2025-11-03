import secrets
import typing as t
from datetime import UTC, datetime, timedelta

from myapp.user import Credentials, PasswordCredentials, SessionInfo, TokenCredentials, UserInfo


class AuthError(Exception):
    pass


class InvalidCredentialsError(AuthError):
    pass


class ExpiredSessionError(AuthError):
    pass


class SimpleInsecureAuthenticator:
    """
    WARNING: THIS AUTHENTICATOR IS NOT FOR PRODUCTION USE!
    """

    def __init__(self, now: t.Callable[[], datetime] | None = None) -> None:
        self.__now = now if now is not None else _get_utc_now
        self.__users = list[UserInfo]()
        self.__sessions = dict[str, tuple[UserInfo, SessionInfo]]()
        self.__session_ttl = timedelta(hours=12)

    def authenticate(self, credentials: Credentials) -> UserInfo:
        match credentials:
            case PasswordCredentials(username=username, password=password):
                user = self.__find_user_by_name(username)
                if user is None or password != user.password:
                    raise InvalidCredentialsError(credentials)

                return user

            case TokenCredentials(token=token):
                pair = self.__sessions.get(token)
                if pair is None:
                    raise InvalidCredentialsError(credentials)

                user, session = pair
                if session.expires_at <= self.__now():
                    self.__sessions.pop(token, None)
                    raise ExpiredSessionError(session)

                return user

            case _:
                t.assert_never(credentials)

    def login(self, credentials: PasswordCredentials) -> SessionInfo:
        user = self.authenticate(credentials)

        now = self.__now()
        session = SessionInfo(
            token=secrets.token_urlsafe(32),
            created_at=now,
            expires_at=now + self.__session_ttl,
        )
        self.__sessions[session.token] = (user, session)

        return session

    def register(self, name: str, password: str) -> UserInfo:
        user = UserInfo(id_=len(self.__users) + 1, name=name, password=password)
        self.__users.append(user)
        return user

    def __find_user_by_name(self, name: str) -> UserInfo | None:
        for user in self.__users:
            if user.name == name:
                return user

        return None


def _get_utc_now() -> datetime:
    return datetime.now(UTC)
