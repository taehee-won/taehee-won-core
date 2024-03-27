from typing import Dict, Final, List, Optional
from requests import request  # pip install requests
from fake_useragent import FakeUserAgent  # pip install fake_useragent

from ..lib.macro import PARAMS, ATTR, KWARG_STR
from ..lib.Trace import Trace
from ..lib.Interval import Interval
from ..lib import datetime
from ..data.OrderedDictList import OrderedDictList

_MARKETS: Final[Dict] = {
    "KOSPI": "STK",
    "KOSDAQ": "KSQ",
}
_START: Final[datetime.dt] = datetime.get(1997, 1, 3)


def get_markets() -> List[str]:
    return list(_MARKETS.keys())


def get_codes(
    market: Optional[str] = None,
    active: Optional[bool] = None,
) -> List[str]:
    return _KRX.assets().items(PARAMS(market=market, active=active)).values("code")


def get_assets(
    market: Optional[str] = None,
    active: Optional[bool] = None,
) -> OrderedDictList:
    attrs = KWARG_STR(market=market, active=active)
    return OrderedDictList(
        "code",
        [
            {
                "market": asset["market"],
                "code": asset["code"],
                "name": asset["name"],
                "active": asset["active"],
            }
            for asset in _KRX.assets().items(PARAMS(market=market, active=active))
        ],
        name=f"KRX.assets({attrs})",
    )


def get_business_days() -> List[datetime.dt]:
    start_str = datetime.to_str(_START, "%Y%m%d")
    end_str = datetime.to_str(
        n
        if (n := datetime.get_now()).hour >= 17
        else datetime.get_before(n, datetime.Period.DAY),
        "%Y%m%d",
    )
    return ATTR(
        _KRX,
        "_business_datetimes",
        lambda: sorted(
            [
                datetime.from_str(quota["TRD_DD"], "%Y/%m/%d")
                for quota in _KRX.request(
                    "dbms/MDC/STAT/standard/MDCSTAT00301",
                    {
                        "indIdx": "1",
                        "indIdx2": "001",
                        "strtDd": start_str,
                        "endDd": end_str,
                    },
                    "output",
                    separate_time=True,
                )
            ]
        ),
    )


def get_assets_quote(
    market: Optional[str] = None,
    target: Optional[datetime.dt] = None,
) -> OrderedDictList:
    business_days = get_business_days()
    if target is None:
        target = business_days[-1]

    if target not in business_days:
        raise TypeError(f"invalid target: {target}")

    markets = [market] if market else get_markets()
    target_str = datetime.to_str(target, "%Y%m%d")

    attrs = KWARG_STR(markets=markets, target=target_str)
    return OrderedDictList(
        "code",
        [
            {
                "code": quote["ISU_SRT_CD"],
                **_KRX.asset_quote(quote),
            }
            for market in markets
            for quote in _KRX.request(
                "dbms/MDC/STAT/standard/MDCSTAT01501",
                {
                    "mktId": _MARKETS[market],
                    "trdDd": target_str,
                },
                "OutBlock_1",
            )
            if _KRX.is_asset_valid_quote(quote)
        ],
        name=f"KRX.quotes({attrs})",
    )


def get_asset_quotes(
    code: str,
    start: Optional[datetime.dt] = None,
    end: Optional[datetime.dt] = None,
) -> OrderedDictList:
    days = get_business_days()
    if start is None:
        start = _START

    if end is None:
        end = days[-1]

    if (
        not (days[0] <= start <= days[-1])
        or not (days[0] <= end <= days[-1])
        or start > end
    ):
        raise TypeError(f"invalid args: {days[0]} <= {start} <= {end} <= {days[-1]}")

    start_str = datetime.to_str(start, "%Y%m%d")
    end_str = datetime.to_str(end, "%Y%m%d")

    asset = _KRX.assets().get(code)
    if asset is None:
        raise TypeError(f"invalid code: {code}")

    attrs = KWARG_STR(code=code, start=start_str, end=end_str)
    return OrderedDictList(
        "datetime",
        [
            {
                "datetime": datetime.from_str(quote["TRD_DD"], "%Y/%m/%d"),
                **_KRX.asset_quote(quote),
            }
            for quote in _KRX.request(
                "dbms/MDC/STAT/standard/MDCSTAT01701",
                {
                    "isuCd": asset["id"],
                    "strtDd": start_str,
                    "endDd": end_str,
                    "adjStkPrc": 2,  # adjusted stock price
                },
                "output",
            )
            if _KRX.is_asset_valid_quote(quote)
        ],
        name=f"KRX.quotes({attrs})",
    )


class _KRX:
    @staticmethod
    def assets() -> OrderedDictList:
        return ATTR(
            _KRX,
            "_assets",
            lambda: OrderedDictList(
                "code",
                [
                    {
                        "market": market,
                        "code": asset["short_code"],
                        "name": asset["codeName"],
                        "active": active,
                        "id": asset["full_code"],
                    }
                    for market, code in _MARKETS.items()
                    for bld, active in {
                        "dbms/comm/finder/finder_stkisu": True,
                        "dbms/comm/finder/finder_listdelisu": False,
                    }.items()
                    for asset in _KRX.request(
                        bld,
                        {"mktsel": code, "typeNo": 0},
                        "block1",
                    )
                    if len(asset["short_code"]) == 6
                ],
                name="KRX.assets",
            ),
        )

    @staticmethod
    def asset_quote(quote: Dict) -> Dict:
        return {
            key: int(quote[response].replace(",", ""))
            for response, key in {
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
    def is_asset_valid_quote(quote: Dict[str, str]) -> bool:
        return bool(quote) and all(
            quote[key] and quote[key] != "0"
            for key in [
                "TDD_OPNPRC",
                "TDD_HGPRC",
                "TDD_LWPRC",
                "TDD_CLSPRC",
                "ACC_TRDVOL",
            ]
        )

    @staticmethod
    def request(bld: str, data: Dict, target: str, separate_time: bool = False) -> List:
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
        method = "POST"

        while "Android" not in (
            u := ATTR(_KRX, "_fake", lambda: FakeUserAgent(verify_ssl=False)).random
        ):
            pass

        if separate_time:
            attrs = []

            s = datetime.from_str(data["strtDd"], "%Y%m%d")
            e = datetime.from_str(data["endDd"], "%Y%m%d")

            while s < e:
                m = datetime.get_before(
                    datetime.get_after(s, datetime.Period.YEAR, 2), datetime.Period.DAY
                )
                attrs.append(
                    {
                        "strtDd": datetime.to_str(s, "%Y%m%d"),
                        "endDd": datetime.to_str(m if m <= e else e, "%Y%m%d"),
                    }
                )
                s = datetime.get_after(s, datetime.Period.YEAR, 2)
        else:
            attrs = [{}]

        response = []
        for attr in attrs:
            ATTR(
                _KRX,
                "_interval",
                lambda: Interval(1, name="KRX"),
            ).interval()

            r = request(
                method,
                url,
                headers={"User-Agent": u},
                data={"bld": bld, **data, **attr},
            )
            if r.status_code != 200:
                raise ValueError(f"request failed: {r.status_code} {bld} {data} {attr}")

            response.extend(r.json()[target])

        ATTR(
            _KRX,
            "_trace",
            lambda: Trace("core"),
        ).debug(f"request {bld} {data} respond {len(response)} {target} data")

        return response
