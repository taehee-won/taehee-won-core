from typing import Union
from enum import Enum
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Datetime:
    class Period(Enum):
        YEAR = "year"
        MONTH = "month"
        WEEK = "week"
        DAY = "day"
        HOUR = "hour"
        MINUTE = "minute"

    def __init__(self, dt: datetime) -> None:
        self._dt = dt

    @property
    def year(self) -> int:
        return self._dt.year

    @property
    def month(self) -> int:
        return self._dt.month

    @property
    def day(self) -> int:
        return self._dt.day

    @property
    def hour(self) -> int:
        return self._dt.hour

    @property
    def minute(self) -> int:
        return self._dt.minute

    def __str__(self) -> str:
        return self.to_str("%Y/%m/%d %H:%M:%S")

    def __eq__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt == value

        elif isinstance(value, Datetime):
            return self._dt == value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

    def __ne__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt != value

        elif isinstance(value, Datetime):
            return self._dt != value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

    def __lt__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt < value

        elif isinstance(value, Datetime):
            return self._dt < value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

    def __le__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt <= value

        elif isinstance(value, Datetime):
            return self._dt <= value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

    def __gt__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt > value

        elif isinstance(value, Datetime):
            return self._dt > value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

    def __ge__(self, value: object) -> bool:
        if isinstance(value, datetime):
            return self._dt >= value

        elif isinstance(value, Datetime):
            return self._dt >= value._dt

        err = f"Invalid type: {type(value)}"
        raise TypeError(err)

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

    def to_datetime(self) -> datetime:
        return self._dt

    def to_str(self, fmt: str) -> str:
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

    def get_quarter_start(self, quarters: int = 0) -> "Datetime":
        dt = self._get_quarter_start(self._dt)

        while quarters:
            if quarters > 0:
                dt += relativedelta(months=3)
                quarters -= 1

            else:
                dt -= timedelta(minutes=1)
                quarters += 1

            dt = self._get_quarter_start(dt)

        return Datetime(dt)

    def get_quarter_end(self, quarters: int = 0) -> "Datetime":
        return self.get_quarter_start(quarters + 1).get_before(self.Period.MINUTE, 1)

    def get_slice(self, period: Union[Period, str] = Period.DAY) -> "Datetime":
        return Datetime(self._get_slice(self._dt, period))

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

    def set_quarter_start(self, quarters: int = 0) -> None:
        self._dt = self._get_quarter_start(self._dt)

        while quarters:
            if quarters > 0:
                self._dt += relativedelta(months=3)
                quarters -= 1

            else:
                self._dt -= timedelta(minutes=1)
                quarters += 1

            self._dt = self._get_quarter_start(self._dt)

    def set_quarter_end(self, quarters: int = 0) -> None:
        self.set_quarter_start(quarters + 1)
        self._dt -= timedelta(minutes=1)

    def set_slice(self, period: Union[Period, str] = Period.DAY) -> None:
        self._dt = self._get_slice(self._dt, period)

    @classmethod
    def _get_delta(
        cls,
        period: Union[Period, str],
        interval: int,
    ) -> Union[timedelta, relativedelta]:
        period = cls.Period(period)

        return {
            cls.Period.DAY: timedelta(days=interval),
            cls.Period.HOUR: timedelta(hours=interval),
            cls.Period.MINUTE: timedelta(minutes=interval),
            cls.Period.WEEK: timedelta(weeks=interval),
            cls.Period.MONTH: relativedelta(months=interval),
            cls.Period.YEAR: relativedelta(years=interval),
        }.get(period, timedelta(days=interval))

    @staticmethod
    def _get_quarter_start(dt: datetime) -> datetime:
        return datetime(dt.year, (dt.month - 1) // 3 * 3 + 1, 1)

    @classmethod
    def _get_slice(
        cls,
        dt: datetime,
        period: Union[Period, str] = Period.DAY,
    ) -> datetime:
        period = cls.Period(period)

        if period == cls.Period.WEEK:
            err = f"Invalid period: {period}"
            raise TypeError(err)

        fmt = "%Y%m%d%H%M"[
            : {
                cls.Period.YEAR: 2,
                cls.Period.MONTH: 4,
                cls.Period.DAY: 6,
                cls.Period.HOUR: 8,
                cls.Period.MINUTE: 10,
            }[period]
        ]

        return datetime.strptime(dt.strftime(fmt), fmt)
