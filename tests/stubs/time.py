from datetime import datetime, timedelta


class ManualTimeTicker:
    def __init__(self, start: datetime) -> None:
        self.__now = start

    def tick(self, step: timedelta) -> datetime:
        self.__now += step
        return self.__now

    def __call__(self) -> datetime:
        return self.__now
