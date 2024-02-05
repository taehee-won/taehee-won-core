from typing import Any, Callable, Dict, Iterable, Optional, Type


def KWARGS(**kwargs: Any) -> Dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def PARAMS(**kwargs: Any) -> Optional[Dict[str, Any]]:
    return params if (params := KWARGS(**kwargs)) else None


def ARGS_STR(*args: Any) -> str:
    return f"{'/'.join(str(arg) for arg in args)}"


def KWARGS_STR(**kwargs: Any) -> str:
    params = {k: v for k, v in kwargs.items() if v is not None}
    return f"{'/'.join([f'{k}:{v}' for k, v in params.items()])}"


def ATTR(obj: object, name: str, initialize: Callable) -> Any:
    if not hasattr(obj, name):
        setattr(obj, name, initialize())

    return getattr(obj, name)


def LOOP(iterable: Iterable) -> None:
    for _ in iterable:
        pass


def CALL(
    func: Callable,
    *args: Any,
    ignore: Type[BaseException],
    **kwargs: Any,
) -> Optional[Any]:
    try:
        return func(*args, **kwargs)

    except ignore:
        return None


def RAISE(exception: Type[BaseException], message: str):
    raise exception(message)
