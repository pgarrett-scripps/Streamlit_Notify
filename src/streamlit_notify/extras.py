"""
Functional API for Streamlit Notify (For Streamlit Extras)
"""

from typing import Any, Literal, Optional

from .queue import NotificationQueue
from . import STATUS_ELEMENTS


def toast_stn(*args: Any, **kwargs: Any) -> None:
    """Display a toast notification."""
    return STATUS_ELEMENTS["toast"](*args, **kwargs)


def balloons_stn(*args: Any, **kwargs: Any) -> None:
    """Display a balloons notification."""
    return STATUS_ELEMENTS["balloons"](*args, **kwargs)


def snow_stn(*args: Any, **kwargs: Any) -> None:
    """Display a snow notification."""
    return STATUS_ELEMENTS["snow"](*args, **kwargs)


def success_stn(*args: Any, **kwargs: Any) -> None:
    """Display a success notification."""
    return STATUS_ELEMENTS["success"](*args, **kwargs)


def info_stn(*args: Any, **kwargs: Any) -> None:
    """Display an info notification."""
    return STATUS_ELEMENTS["info"](*args, **kwargs)


def error_stn(*args: Any, **kwargs: Any) -> None:
    """Display an error notification."""
    return STATUS_ELEMENTS["error"](*args, **kwargs)


def warning_stn(*args: Any, **kwargs: Any) -> None:
    """Display a warning notification."""
    return STATUS_ELEMENTS["warning"](*args, **kwargs)


def exception_stn(*args: Any, **kwargs: Any) -> None:
    """Display an exception notification."""
    return STATUS_ELEMENTS["exception"](*args, **kwargs)


def notify(
    remove: bool = True,
    element: Optional[
        Literal[
            "toast",
            "balloons",
            "snow",
            "success",
            "info",
            "error",
            "warning",
            "exception",
        ]
    ] = None,
) -> None:
    """
    Display queued notifications.
    """
    if element is None:
        for widget in STATUS_ELEMENTS.values():
            widget.notify(remove=remove)
    elif element in STATUS_ELEMENTS:
        STATUS_ELEMENTS[element].notify(remove=remove)
    else:
        raise ValueError(
            f"Invalid filter: {element}. Must be one of {list(STATUS_ELEMENTS.keys())}."
        )


def get_notifications(
    element: Literal[
        "toast",
        "balloons",
        "snow",
        "success",
        "info",
        "error",
        "warning",
        "exception",
    ],
) -> NotificationQueue:
    """
    Retrieve notifications for a specific type.
    """
    return STATUS_ELEMENTS[element].notifications
