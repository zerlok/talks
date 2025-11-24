import pytest


class User:
    pass


class Project:
    pass


class UserRepository:
    def create(self, name: str) -> User:
        pass


class ProjectRepository:
    def create(self, name: str) -> Project:
        pass


@pytest.fixture
def cleanup_tables() -> None:
    pass  # cleanup logic


@pytest.fixture
def user_repo(cleanup_tables: None) -> UserRepository:
    return UserRepository()


@pytest.fixture
def project_repo(cleanup_tables: None) -> ProjectRepository:
    return ProjectRepository()


@pytest.fixture
def user_john(user_repo: UserRepository) -> User:
    return user_repo.create("John")


@pytest.fixture
def simple_project(project_repo: ProjectRepository) -> Project:
    return project_repo.create("Simple")


def test_it(
    user_john: User,
    simple_project: Project,
) -> None:
    pass


@pytest.fixture
def root_value() -> str:
    print("root")
    return "root"


@pytest.fixture
def left_value(root_value: str) -> str:
    print("left")
    return "left"


@pytest.fixture
def right_value(root_value: str) -> str:
    print("right")
    return "right"


@pytest.fixture
def join_value(left_value: str, right_value: str) -> str:
    print("join")
    return f"{left_value} {right_value}"


def test_order(join_value: str) -> None:
    assert join_value == "left right"
