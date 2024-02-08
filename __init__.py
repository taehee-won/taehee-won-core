from .src.library.data.Datetime import Period, Datetime
from .src.library.data.DictList import DictListFile, DictList
from .src.library.data.OrderedDictList import OrderedDictList
from .src.library.lib.Lib import Lib
from .src.library.lib.Math import Math
from .src.library.lib.OS import OS
from .src.library.lib.Interval import Interval
from .src.library.lib.LinkedInterval import LinkedInterval
from .src.library.lib.Trace import TraceLevel, Trace
from .src.library.lib.macro import KWARGS, ARGS_STR, KWARGS_STR, ATTR, LOOP, CALL, RAISE

__all__ = []
__all__.extend(["Period", "Datetime"])
__all__.extend(["DictListFile", "DictList", "OrderedDictList"])
__all__.extend(["Lib", "Math", "OS"])
__all__.extend(["Interval", "LinkedInterval"])
__all__.extend(["TraceLevel", "Trace"])
__all__.extend(["KWARGS", "ARGS_STR", "KWARGS_STR", "ATTR", "LOOP", "CALL", "RAISE"])


__author__ = "Taehee Won(taehee.won@gmail.com)"
__url__ = "https://github.com/taehee-won/taehee-won-core"
__version__ = "0.0.1"
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
