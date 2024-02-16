from typing import Union
from enum import Enum

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Period(Enum):
    YEAR = "year"
    MONTH = "month"
    WEEK = "week"
    DAY = "day"
    HOUR = "hour"
    MINUTE = "minute"


class Datetime:
    def __init__(self, dt: datetime) -> None:
        self._dt: datetime = dt

    @classmethod
    def from_values(
        cls,
        year: int,
        month: int = 1,
        day: int = 1,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ) -> "Datetime":
        return cls(datetime(year, month, day, hour, minute, second))

    @classmethod
    def from_now(cls) -> "Datetime":
        return cls(datetime.now())

    @classmethod
    def from_str(cls, string: str, fmt: str) -> "Datetime":
        return cls(datetime.strptime(string, fmt))

    @classmethod
    def from_timestamp(cls, timestamp: float) -> "Datetime":
        return cls(datetime.fromtimestamp(timestamp))

    def get_datetime(self) -> datetime:
        return self._dt

    def get_str(self, fmt: str) -> str:
        return self._dt.strftime(fmt)

    def get_before(
        self,
        period: Union[Period, str] = Period.DAY,
        interval: int = 1,
    ) -> "Datetime":
        return Datetime(self._dt - self._get_delta(period, interval))

    def get_after(
        self,
        period: Union[Period, str] = Period.DAY,
        interval: int = 1,
    ) -> "Datetime":
        return Datetime(self._dt + self._get_delta(period, interval))

    def get_quarter_start(self, index: int = 0) -> "Datetime":
        dt = self._get_quarter_start(self._dt)

        while index:
            if index > 0:
                dt += relativedelta(months=3)
                index -= 1

            else:
                dt -= timedelta(days=1)
                index += 1

            dt = self._get_quarter_start(dt)

        return Datetime(dt)

    def get_quarter_end(self, index: int = 0) -> "Datetime":
        dt = self.get_quarter_start(index + 1)
        dt.set_before(Period.DAY, 1)

        return dt

    def set_before(
        self,
        period: Union[Period, str] = Period.DAY,
        interval: int = 1,
    ) -> None:
        self._dt -= self._get_delta(period, interval)

    def set_after(
        self,
        period: Union[Period, str] = Period.DAY,
        interval: int = 1,
    ) -> None:
        self._dt += self._get_delta(period, interval)

    def set_quarter_start(self, index: int = 0) -> None:
        self._dt = self._get_quarter_start(self._dt)

        while index:
            if index > 0:
                self._dt += relativedelta(months=3)
                index -= 1

            else:
                self._dt -= timedelta(days=1)
                index += 1

            self._dt = self._get_quarter_start(self._dt)

    def set_quarter_end(self, index: int = 0) -> None:
        self.set_quarter_start(index + 1)
        self._dt -= timedelta(days=1)

    def extract(self, fmt: str) -> None:
        self._dt = datetime.strptime(self._dt.strftime(fmt), fmt)

    @staticmethod
    def _get_delta(
        period: Union[Period, str],
        interval: int,
    ) -> Union[timedelta, relativedelta]:
        if isinstance(period, str):
            period = Period(period)

        return {
            Period.DAY: timedelta(days=interval),
            Period.HOUR: timedelta(hours=interval),
            Period.MINUTE: timedelta(minutes=interval),
            Period.WEEK: timedelta(weeks=interval),
            Period.MONTH: relativedelta(months=interval),
            Period.YEAR: relativedelta(years=interval),
        }.get(period, timedelta(days=interval))

    @staticmethod
    def _get_quarter_start(dt: datetime) -> datetime:
        return datetime(dt.year, (dt.month - 1) // 3 * 3 + 1, 1)
