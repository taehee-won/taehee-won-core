from typing import List, Dict, Optional, Union
from requests import request
from datetime import datetime

from ..lib.macro import ATTR, KWARGS_STR, PARAMS
from ..lib.Trace import Trace
from ..lib.Interval import Interval
from ..lib.Datetime import Datetime
from ..data.OrderedDictList import OrderedDictList


class KRX:
    @classmethod
    def get_assets(
        cls,
        market: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[Dict[str, str]]:
        return [
            {
                key: asset[key]
                for key in [
                    "market",
                    "code",
                    "name",
                    "active",
                ]
            }
            for asset in cls._get_assets().get_data(
                PARAMS(market=market, active=active)
            )
        ]

    @classmethod
    def get_markets(cls) -> List[str]:
        return list(cls._get_attrs()["markets"].keys())

    @classmethod
    def get_codes(
        cls,
        market: Optional[str] = None,
        active: Optional[bool] = None,
    ) -> List[str]:
        return [
            asset["code"]
            for asset in cls._get_assets().get_data(
                PARAMS(market=market, active=active)
            )
        ]

    @classmethod
    def get_days(cls) -> List[datetime]:
        return ATTR(
            cls,
            "days",
            lambda: sorted(
                [
                    Datetime.from_str(index["TRD_DD"], "%Y/%m/%d").to_datetime()
                    for start, end in cls._split_period(
                        cls._get_attrs()["start"], cls._get_attrs()["end"]
                    )
                    for index in cls._request(
                        "output",
                        bld="dbms/MDC/STAT/standard/MDCSTAT00301",
                        indIdx="1",
                        indIdx2="001",
                        strtDd=start.to_str("%Y%m%d"),
                        endDd=end.to_str("%Y%m%d"),
                    )
                ]
            ),
        )

    @classmethod
    def get_assets_candles(
        cls,
        market: Optional[str] = None,
        date: Optional[Union[datetime, Datetime]] = None,
    ) -> List:
        days = cls.get_days()

        d = (Datetime(date) if isinstance(date, datetime) else date) if date else Datetime(days[-1])  # type: ignore
        if d not in days:
            err = f"Invalid date: {d}"
            ATTR(cls, "trace", lambda: Trace("core")).critical(err)
            raise ValueError(err)

        return [
            {
                "code": candle["ISU_SRT_CD"],
                **cls._convert_candle(candle),
            }
            for mktId in (
                [cls._get_attrs()["markets"][market]]
                if market
                else cls._get_attrs()["markets"].values()
            )
            for candle in cls._request(
                "OutBlock_1",
                bld="dbms/MDC/STAT/standard/MDCSTAT01501",
                mktId=mktId,
                trdDd=d.to_str("%Y%m%d"),
            )
            if cls._is_valid_candle(candle)
        ]

    @classmethod
    def get_asset_candles(
        cls,
        code: str,
        start: Optional[Union[datetime, Datetime]] = None,
        end: Optional[Union[datetime, Datetime]] = None,
    ) -> List:
        days = cls.get_days()

        s = (Datetime(start) if isinstance(start, datetime) else start) if start else Datetime(days[0])  # type: ignore
        e = (Datetime(end) if isinstance(end, datetime) else end) if end else Datetime(days[-1])  # type: ignore
        if (
            (not s <= e)
            or (not days[0] <= s <= days[-1])
            or (not days[0] <= e <= days[-1])
        ):
            err = f"Invalid period: start({s.to_str('%Y%m%d')}), end({e.to_str('%Y%m%d')})"
            ATTR(cls, "trace", lambda: Trace("core")).critical(err)
            raise ValueError(err)

        asset = cls._get_assets().get_element(code)
        if asset is None:
            err = f"Invalid code: {code}"
            ATTR(cls, "trace", lambda: Trace("core")).critical(err)
            raise ValueError(err)

        return sorted(
            [
                {
                    "datetime": Datetime.from_str(
                        candle["TRD_DD"],
                        "%Y/%m/%d",
                    ).to_datetime(),
                    **cls._convert_candle(candle),
                }
                for candle in cls._request(
                    "output",
                    bld="dbms/MDC/STAT/standard/MDCSTAT01701",
                    isuCd=asset["id"],
                    strtDd=s.to_str("%Y%m%d"),
                    endDd=e.to_str("%Y%m%d"),
                    adjStkPrc=2,  # adjusted stock price
                )
                if cls._is_valid_candle(candle)
            ],
            key=lambda candle: candle["datetime"],
        )

    @classmethod
    def _get_attrs(cls) -> Dict:
        return ATTR(
            cls,
            "attrs",
            lambda: {
                "markets": {
                    "KOSPI": "STK",
                    "KOSDAQ": "KSQ",
                },
                "start": Datetime.from_values(1997),
                "end": (
                    now
                    if (now := Datetime.from_now()).hour >= 17
                    else now.get_before(Datetime.Period.DAY)
                ).get_slice(Datetime.Period.DAY),
            },
        )

    @classmethod
    def _get_assets(cls) -> OrderedDictList:
        return ATTR(
            cls,
            "assets",
            lambda: OrderedDictList(
                "code",
                [
                    {
                        "market": market,
                        "active": active,
                        **{
                            key: asset[field]
                            for field, key in {
                                "short_code": "code",
                                "full_code": "id",
                                "codeName": "name",
                            }.items()
                        },
                    }
                    for market, mktsel in cls._get_attrs()["markets"].items()
                    for active, bld in {
                        True: "dbms/comm/finder/finder_stkisu",
                        False: "dbms/comm/finder/finder_listdelisu",
                    }.items()
                    for asset in cls._request(
                        "block1", bld=bld, mktsel=mktsel, typeNo=0
                    )
                    if len(asset["short_code"]) == 6
                ],
                name="KRX.assets",
            ),
        )

    @classmethod
    def _request(cls, key: str, **kwargs) -> List:
        trace = ATTR(cls, "trace", lambda: Trace("core"))

        ATTR(cls, "interval", lambda: Interval(1, name="core.KRX")).wait()

        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        method = "POST"
        response = request(method, url, data=kwargs)

        if response.status_code != 200:
            err = (
                f"Request failed: {response.status_code}"
                + f" for {method}({url})({kwargs})"
            )
            trace.critical(err)
            raise ValueError(err)

        data = response.json()[key]
        trace.debug(
            f"request {method}(url)({KWARGS_STR(**kwargs)}) response"
            + f" {key} {len(data)} data"
        )

        return data

    @classmethod
    def _split_period(cls, start: Datetime, end: Datetime) -> List:
        if not start <= end:
            err = f"Invalid period: start({start}), end({end})"
            ATTR(cls, "trace", lambda: Trace("core")).critical(err)
            raise ValueError(err)

        s = start
        e = end
        periods = []

        while s <= e:
            c = s.get_after(Datetime.Period.YEAR, 2).get_before(Datetime.Period.DAY, 1)
            if e <= c:
                periods.append([s, e])
                break

            periods.append([s, c])
            s = s.get_after(Datetime.Period.YEAR, 2)

        return periods

    @staticmethod
    def _convert_candle(candle: Dict[str, str]) -> Dict[str, int]:
        return {
            key: int(candle[field].replace(",", ""))
            for field, key in {
                "TDD_OPNPRC": "open",
                "TDD_HGPRC": "high",
                "TDD_LWPRC": "low",
                "TDD_CLSPRC": "close",
                "ACC_TRDVOL": "volume",
                "ACC_TRDVAL": "expense",
                "MKTCAP": "capitalization",
            }.items()
        }

    @staticmethod
    def _is_valid_candle(candle: Dict[str, str]) -> bool:
        return all(
            candle[key] and candle[key] != "0"
            for key in [
                "TDD_OPNPRC",
                "TDD_HGPRC",
                "TDD_LWPRC",
                "TDD_CLSPRC",
                "ACC_TRDVOL",
                "ACC_TRDVAL",
                "MKTCAP",
            ]
        )
