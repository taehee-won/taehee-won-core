from .library.macro import KWARGS, PARAMS, ARGS_STR, KWARGS_STR
from .library.macro import ATTR, LOOP, CALL, RAISE
from .library.Lib import Lib
from .library.Math import Math
from .library.OS import OS
from .library.Interface import Interface
from .library.Interval import Interval
from .library.Process import Process
from .library.Files import Files
from .library.Trace import Trace
from .library.Datetime import Datetime
from .database.MongoDB import MongoDB
from .framework.Main import Main
from .framework.Executor import Executor

from .data.DictList import DictList
from .data.OrderedDictList import OrderedDictList
from .data.HandledDictList import HandledDictList
from .data.LinkedDictList import LinkedDictList
from .data.handle.Aggregate import Aggregate
from .data.handle.Calculate import Calculate
from .data.handle.Compare import Compare
from .data.handle.Cross import Cross

from .trade.KRX import KRX
from .trade.Upbit import Upbit
from .trade.handle.MA import MA
from .trade.handle.RSI import RSI

__all__ = []
__all__.extend(["KWARGS", "PARAMS", "ARGS_STR", "KWARGS_STR"])
__all__.extend(["ATTR", "LOOP", "CALL", "RAISE"])
__all__.extend(["Lib", "Math", "OS", "Interface", "Interval", "Process", "Trace"])
__all__.extend(["Datetime", "Files"])
__all__.extend(["MongoDB"])
__all__.extend(["Main", "Executor"])
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
