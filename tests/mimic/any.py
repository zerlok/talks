import typing as t

T = t.TypeVar("T")


# NOTE: improved `unittest.mock.ANY`
class _AnyValue:
    def __init__(self, predicate: t.Callable[[object], bool]) -> None:
        self.__predicate = predicate

    @t.override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__predicate!r})"

    @t.override
    def __eq__(self, other: object) -> bool:
        return self.__predicate(other)


def any_value() -> t.Any:
    def check(_: object) -> bool:
        return True

    return t.cast("t.Any", _AnyValue(check))


def of_type(type_: type[T]) -> T:
    def check(obj: object) -> bool:
        return isinstance(obj, type_)

    return t.cast("T", _AnyValue(check))
