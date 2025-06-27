"""
Functional API for Streamlit Notify (For Streamlit Extras)
"""

from typing import Any, Iterable, List, Literal, Optional, Union

from .dclass import StatusElementNotification
from .queue import NotificationQueue
from . import STATUS_ELEMENTS

NotificationType = Literal[
    "toast", "balloons", "snow", "success", "info", "error", "warning", "exception"
]


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
    notification_type: Optional[
        Union[NotificationType, Iterable[NotificationType]]
    ] = None,
) -> None:
    """
    Display queued notifications.
    """
    types = (
        list(STATUS_ELEMENTS.keys())
        if notification_type is None
        else (
            [notification_type]
            if isinstance(notification_type, str)
            else list(notification_type)
        )
    )
    for nt in types:
        if nt in STATUS_ELEMENTS:
            STATUS_ELEMENTS[nt].notify(remove=remove)
        else:
            raise ValueError(
                f"Invalid filter: {nt}. Must be one of {list(STATUS_ELEMENTS.keys())}."
            )


def create_notification(
    *args: Any,
    **kwargs: Any,
) -> StatusElementNotification:
    """
    Create a notification without adding it to the queue.
    """

    notification_type = kwargs.pop("notification_type", None)
    if notification_type is None:
        raise ValueError("notification_type must be provided as a keyword argument.")

    if notification_type in STATUS_ELEMENTS:
        return STATUS_ELEMENTS[notification_type].create_notification(*args, **kwargs)
    else:
        raise ValueError(
            f"Invalid element: {notification_type}. Must be one of {list(STATUS_ELEMENTS.keys())}."
        )


def get_notifications(
    notification_type: Optional[
        Union[NotificationType, Iterable[NotificationType]]
    ] = None,
) -> List[StatusElementNotification]:
    if notification_type is None:
        return [
            n
            for widget in STATUS_ELEMENTS.values()
            for n in widget.notifications.get_all()
        ]
    if isinstance(notification_type, str):
        if notification_type in STATUS_ELEMENTS:
            return STATUS_ELEMENTS[notification_type].notifications.get_all()
        raise ValueError(
            f"Invalid filter: {notification_type}. Must be one of {list(STATUS_ELEMENTS.keys())}."
        )
    try:
        return [
            n
            for nt in notification_type
            if nt in STATUS_ELEMENTS
            for n in STATUS_ELEMENTS[nt].notifications.get_all()
        ]
    except Exception:
        raise ValueError(
            f"Invalid filter: {notification_type}. Must be one of {list(STATUS_ELEMENTS.keys())}."
        )


def get_notification_queue(notification_type: NotificationType) -> NotificationQueue:
    """
    Retrieve notifications for a specific type.
    """
    return STATUS_ELEMENTS[notification_type].notifications
