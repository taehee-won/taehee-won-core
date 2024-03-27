from typing import List, Dict, Optional
from requests import request
from datetime import datetime

from ..lib.macro import ATTR, KWARGS_STR
from ..lib.Trace import Trace
from ..lib.Interval import Interval
from ..lib.Datetime import Datetime, Period


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
            for asset in cls._get_assets()
            if (market is None or asset["market"] == market)
            and (active is None or asset["active"] == active)
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
            for asset in cls._get_assets()
            if (market is None or asset["market"] == market)
            and (active is None or asset["active"] == active)
        ]

    @classmethod
    def get_business_days(cls) -> List[datetime]:
        if not hasattr(cls, "business_days"):
            periods = cls._split_period(
                cls._get_attrs()["start"],
                cls._get_attrs()["end"],
            )

            days = []

            setattr(cls, "business_days", days)

        return getattr(cls, "business_days")

        return ATTR(
            cls,
            "business_days",
            lambda: [
                quota
                for quota in cls._request(
                    "output",
                    bld="dbms/MDC/STAT/standard/MDCSTAT00301",
                    indIdx="1",
                    indIdx2="001",
                    strtDd=cls._get_attrs()["start"].get_str("%Y%m%d"),
                    endDd=cls._get_attrs()["end"].get_str("%Y%m%d"),
                )
            ],
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
                    now if (now := Datetime.from_now()).hour >= 17 else now.get_before()
                ).get_slice(),
            },
        )

    @classmethod
    def _get_assets(cls) -> List[Dict[str, str]]:
        return ATTR(
            cls,
            "assets",
            lambda: [
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
                for asset in cls._request("block1", bld=bld, mktsel=mktsel, typeNo=0)
                if len(asset["short_code"]) == 6
            ],
        )

    @classmethod
    def _request(cls, key: str, **kwargs) -> List:
        trace = ATTR(cls, "trace", lambda: Trace("core"))

        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        method = "POST"

        ATTR(cls, "interval", lambda: Interval(1, name="core.KRX")).wait()

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
            f"request {method}({url})({KWARGS_STR(**kwargs)}) response"
            + f" {key} {len(data)} data"
        )

        return data

    @classmethod
    def _split_period(cls, start: Datetime, end: Datetime) -> List[Datetime]:
        if not start <= end:
            err = f"Invaild period: start({start}), end({end})"
            ATTR(cls, "trace", lambda: Trace("core")).critical(err)
            raise ValueError(err)

        periods = [start]

        while start < end:
            step = start.get_after(Period.YEAR, 2).get_before(Period.DAY, 1)
            if end <= step:
                break

            periods.append(step)
            start = step.get_after()

        periods.append(end)

        return periods
