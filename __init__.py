from .src.library.macro import KWARGS, PARAMS, ARGS_STR, KWARGS_STR
from .src.library.macro import ATTR, LOOP, CALL, RAISE
from .src.library.Lib import Lib
from .src.library.Math import Math
from .src.library.OS import OS
from .src.library.Interface import Interface
from .src.library.Interval import Interval
from .src.library.Process import Process
from .src.library.Trace import Trace
from .src.library.Datetime import Datetime
from .src.database.MongoDB import MongoDB
from .src.framework.Main import Main

from .src.data.DictList import DictList
from .src.data.OrderedDictList import OrderedDictList
from .src.data.HandledDictList import HandledDictList
from .src.data.LinkedDictList import LinkedDictList
from .src.data.handle.Aggregate import Aggregate
from .src.data.handle.Calculate import Calculate
from .src.data.handle.Compare import Compare
from .src.data.handle.Cross import Cross

from .src.trade.KRX import KRX
from .src.trade.Upbit import Upbit
from .src.trade.handle.MA import MA
from .src.trade.handle.RSI import RSI

__all__ = []
__all__.extend(["KWARGS", "PARAMS", "ARGS_STR", "KWARGS_STR"])
__all__.extend(["ATTR", "LOOP", "CALL", "RAISE"])
__all__.extend(["Lib", "Math", "OS", "Interface", "Interval", "Process", "Trace"])
__all__.extend(["Datetime"])
__all__.extend(["MongoDB"])
__all__.extend(["Main"])
__all__.extend(["DictList", "OrderedDictList", "HandledDictList", "LinkedDictList"])
__all__.extend(["Aggregate", "Calculate", "Compare", "Cross"])
__all__.extend(["KRX", "Upbit"])
__all__.extend(["MA", "RSI"])


__author__ = "Taehee Won(taehee.won@gmail.com)"
__url__ = "https://github.com/taehee-won/taehee-won-core"
__version__ = "0.0.4"
__description__ = """
taehee-won-core is a versatile Python framework designed to streamline
and enhance Python programming tasks.  It offers a wide range of utility functions
and modular components that cater to various needs in data handling,
database management, and more. With its focus on flexibility and efficiency,
this framework simplifies the development process, enabling rapid
and effective project implementation. Ideal for both simple scripts
and complex applications, taehee-won-core is a robust solution
for Python developers seeking to optimize code structure and functionality.
"""
