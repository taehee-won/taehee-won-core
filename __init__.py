from .src.library.lib.macro import KWARGS, PARAMS, ARGS_STR, KWARGS_STR
from .src.library.lib.macro import ATTR, LOOP, CALL, RAISE
from .src.library.lib.Lib import Lib
from .src.library.lib.Math import Math
from .src.library.lib.OS import OS
from .src.library.lib.Interface import Interface
from .src.library.lib.Interval import Interval
from .src.library.lib.Process import Process
from .src.library.lib.Datetime import Period, Datetime
from .src.library.lib.Trace import TraceLevel, Trace
from .src.library.data.DictList import DictList
from .src.library.data.OrderedDictList import OrderedDictList
from .src.library.data.HandledDictList import HandledDictList
from .src.library.data.LinkedDictList import LinkedDictList
from .src.library.database.MongoDB import MongoDB
from .src.library.trade.KRX import KRX
from .src.library.trade.Upbit import Upbit
from .src.framework.Component import Component
from .src.framework.main import FrontEnd, main

__all__ = []
__all__.extend(["KWARGS", "PARAMS", "ARGS_STR", "KWARGS_STR"])
__all__.extend(["ATTR", "LOOP", "CALL", "RAISE"])
__all__.extend(["Lib", "Math", "OS", "Interface", "Interval", "Process"])
__all__.extend(["Period", "Datetime"])
__all__.extend(["TraceLevel", "Trace"])
__all__.extend(["DictList", "OrderedDictList", "HandledDictList", "LinkedDictList"])
__all__.extend(["MongoDB"])
__all__.extend(["KRX", "Upbit"])
__all__.extend(["Component", "FrontEnd", "main"])


__author__ = "Taehee Won(taehee.won@gmail.com)"
__url__ = "https://github.com/taehee-won/taehee-won-core"
__version__ = "0.0.3"
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
