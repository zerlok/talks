from myapp.user import Credentials, UserInfo


class SimpleAuthenticator:
    def __init__(self) -> None:
        self.__users = list[UserInfo]()

    def authenticate(self, credentials: Credentials) -> UserInfo | None:
        user = self.__find_user_by_name(credentials.username)
        return user if user is not None and credentials.password == user.password else None

    def register(self, name: str, password: str) -> UserInfo:
        user = UserInfo(id_=len(self.__users) + 1, name=name, password=password)
        self.__users.append(user)
        return user

    def __find_user_by_name(self, name: str) -> UserInfo | None:
        for user in self.__users:
            if user.name == name:
                return user

        return None
