from typing import Optional, List, Dict, Union, Any
from enum import Enum
from requests import request
from datetime import datetime

from ..library.macro import ATTR, KWARGS
from ..library.Trace import Trace
from ..library.Interval import Interval
from ..library.Datetime import Datetime


class Upbit:
    class Period(Enum):
        MONTH = "month"
        WEEK = "week"
        DAY = "day"
        MINUTE = "minute"

    # reference: https://docs.upbit.com/reference/마켓-코드-조회
    # url      : https://api.upbit.com/v1/market/all
    # method   : GET
    # params   : isDetails(bool)
    # response : 200(json), 400(object)
    # fields   : market, korean_name, english_name
    # return   : code, en, ko

    @classmethod
    def get_assets(cls) -> List[Dict[str, str]]:
        url = "https://api.upbit.com/v1/market/all"
        method = "GET"
        params = {"isDetails": "false"}

        return ATTR(
            cls,
            "assets",
            lambda: [
                {
                    key: asset[field]
                    for field, key in {
                        "market": "code",
                        "english_name": "en",
                        "korean_name": "ko",
                    }.items()
                }
                for asset in cls._request(url, method, params).data
            ],
        )

    @classmethod
    def get_codes(cls) -> List[Dict[str, str]]:
        return ATTR(cls, "codes", lambda: [asset["code"] for asset in cls.get_assets()])

    # reference: https://docs.upbit.com/v1.4.0/reference/분minute-캔들-1
    # reference: https://docs.upbit.com/v1.4.0/reference/일day-캔들-1
    # reference: https://docs.upbit.com/v1.4.0/reference/주week-캔들-1
    # reference: https://docs.upbit.com/v1.4.0/reference/월month-캔들-1
    # url      : https://api.upbit.com/v1/candles/minutes/{unit}
    # url      : https://api.upbit.com/v1/candles/days
    # url      : https://api.upbit.com/v1/candles/weeks
    # url      : https://api.upbit.com/v1/candles/months
    # method   : GET
    # params   : market(str), count(int, max:200), to(optional, yyyy-MM-dd HH:mm:ss)
    #          + day: convertingPriceUnit
    # response : 200(json), 400(object)
    # fields   : market, candle_date_time_utc, candle_date_time_kst,
    #            opening_price, high_price, low_price, trade_price,
    #            timestamp, candle_acc_trade_price, candle_acc_trade_volume
    #          + minute: unit
    #          + day   : change_price, change_rate, converted_trade_price
    #          + week  : first_day_of_period
    # return   : datetime, open, high, low, close, volume

    @classmethod
    def get_candles(
        cls,
        code: str,
        period: Union[Period, str] = Period.DAY,
        unit: int = 1,
        start: Optional[Union[datetime, Datetime]] = None,
        end: Optional[Union[datetime, Datetime]] = None,
    ) -> List[Dict[str, Any]]:
        trace = ATTR(cls, "trace", lambda: Trace("core"))

        period = cls.Period(period)

        if (period != cls.Period.MINUTE and unit != 1) or (
            unit not in [1, 3, 5, 15, 10, 30, 60, 240]
        ):
            err = f"Invalid unit: {unit} for {period}"
            trace.critical(err)
            raise TypeError(err)

        url = f"https://api.upbit.com/v1/candles/{period.value}s"
        if period == cls.Period.MINUTE:
            url += f"/{unit}"

        method = "GET"
        params = {
            "market": code,
            "count": 200,
            "to": (
                (Datetime(end) if isinstance(end, datetime) else end)
                .get_before(Datetime.Period.HOUR, 9)
                .get_after(Datetime.Period.MINUTE, 1)
                .to_str("%Y-%m-%d %H:%M:%S")
                if end
                else None
            ),
        }

        candles = []
        response = cls._request(url, method, params)
        start_datetime = response.datetime
        while response.data:
            data = [
                {
                    "datetime": Datetime.from_str(
                        candle["candle_date_time_kst"],
                        "%Y-%m-%dT%H:%M:%S",
                    ).to_datetime(),
                    **{
                        key: candle[field]
                        for field, key in {
                            "opening_price": "open",
                            "high_price": "high",
                            "low_price": "low",
                            "trade_price": "close",
                            "candle_acc_trade_volume": "volume",
                        }.items()
                    },
                }
                for candle in response.data
            ]

            if start and any(candle["datetime"] < start for candle in data):
                candles.extend(candle for candle in data if start <= candle["datetime"])
                break

            candles.extend(data)

            params["to"] = (
                Datetime(candles[-1]["datetime"])
                .set_before(Datetime.Period.HOUR, 9)
                .to_str("%Y-%m-%d %H:%M:%S")
            )
            response = cls._request(url, method, params)

        candles.reverse()
        if (
            candles
            and start_datetime.get_before(Datetime.Period(period.value), unit)
            < candles[-1]["datetime"]
        ):
            candles.pop()

        return [
            candle
            for candle in candles
            if all(candle[key] for key in ["open", "high", "low", "close", "volume"])
        ]

    @classmethod
    def _request(
        cls,
        url: str,
        method: str,
        params: Optional[Dict] = None,
    ) -> "_Response":
        trace = ATTR(cls, "trace", lambda: Trace("core"))

        ATTR(cls, "interval", lambda: Interval({1: 9}, name="core.Upbit")).wait()

        headers = {"accept": "application/json"}
        response = request(method, url, headers=headers, **KWARGS(params=params))

        if response.status_code != 200:
            err = f"Request failed: {response.status_code} for {method}({url})"
            trace.critical(err)
            raise ValueError(err)

        data = response.json()
        datetime = Datetime.from_str(
            response.headers["date"],
            "%a, %d %b %Y %H:%M:%S GMT",
        ).set_after(Datetime.Period.HOUR, 9)

        response = _Response(datetime, data)
        trace.debug(f"request {method}({url}) response {response}")

        return response


class _Response:
    def __init__(self, datetime: Datetime, data: List) -> None:
        self._datetime = datetime
        self._data = data

    def __str__(self) -> str:
        return f"{len(self._data)} data at {self._datetime}"

    @property
    def datetime(self) -> Datetime:
        return self._datetime

    @property
    def data(self) -> List:
        return self._data
