from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, kw_only=True)
class PasswordCredentials:
    username: str
    password: str = field(repr=False)


@dataclass(frozen=True, kw_only=True)
class TokenCredentials:
    token: str = field(repr=False)


@dataclass(frozen=True, kw_only=True)
class UserInfo:
    id_: int
    name: str
    password: str = field(repr=False)


@dataclass(frozen=True, kw_only=True)
class SessionInfo(TokenCredentials):
    created_at: datetime
    expires_at: datetime


# noinspection PyCompatibility
type Credentials = PasswordCredentials | TokenCredentials
