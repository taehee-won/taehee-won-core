from unittest import TestCase, skipIf
from os import environ

from src.library.lib.Trace import TraceLevel, Trace
from src.library.trade.KRX import KRX


@skipIf(
    environ.get("TEST_INTERNET") != "1" and environ.get("TEST_ALL") != "1",
    "KRX needs internet connection",
)
class TestKRX(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    # def test_get_assets(self):
    #     print("asset", KRX.get_assets()[0], len(KRX.get_assets()))

    # def test_get_markets(self):
    #     print("market", KRX.get_markets()[0], len(KRX.get_markets()))

    # def test_get_codes(self):
    #     print("code", KRX.get_codes()[0], len(KRX.get_codes()))

    def test_get_business_days(self):
        print("days", KRX.get_business_days()[0], len(KRX.get_business_days()))
