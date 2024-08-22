from typing import Callable, ParamSpec, TypeVar
import time, datetime, warnings

def spin_until(t: float, interval: float = 0.5):
    while True:
        if time.time() >= t:
            break
        time.sleep(interval)

def spin_until_date(d: datetime.datetime, interval: float = 0.5):
    spin_until(d.timestamp(), interval=interval)

P = ParamSpec('P'); R = TypeVar('R')
def supress_warning(wt: type[Warning] | None = None):
    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        def result(*args: P.args, **kwargs: P.kwargs) -> R:
            with warnings.catch_warnings():
                if wt is not None:
                    warnings.filterwarnings("ignore", category=wt)
                else:
                    warnings.simplefilter("ignore")
                return f(*args, **kwargs)
        return result
    return decorator
