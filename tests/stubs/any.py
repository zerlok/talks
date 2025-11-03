import typing as t

T = t.TypeVar("T")


# NOTE: improved `unittest.mock.ANY`
class _AnyValue:
    def __init__(self, predicate: t.Callable[[object], bool]) -> None:
        self.__predicate = predicate

    @t.override
    def __eq__(self, other: object) -> bool:
        return self.__predicate(other)


def create_any(predicate: t.Callable[[object], bool]) -> t.Any:
    return t.cast("t.Any", _AnyValue(predicate))


def any_value() -> t.Any:
    def check(obj: object) -> bool:
        return True

    return t.cast("t.Any", _AnyValue(check))


def any_of_type(of_type: type[T]) -> T:
    def check(obj: object) -> bool:
        return isinstance(obj, of_type)

    return t.cast("T", _AnyValue(check))
