from dataclasses import dataclass, field


@dataclass(frozen=True, kw_only=True)
class UserInfo:
    id_: int
    name: str
    password: str = field(repr=False)


@dataclass(frozen=True, kw_only=True)
class Credentials:
    username: str
    password: str = field(repr=False)
