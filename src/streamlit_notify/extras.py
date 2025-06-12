
from typing import Any
from . import STATUS_ELEMENTS

def toast_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a toast notification.
    """
    return STATUS_ELEMENTS["toast"](*args, **kwargs)