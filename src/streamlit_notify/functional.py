"""
Functional API for Streamlit Notify (For Streamlit Extras)
"""

from typing import Any, Iterable, List, Literal, Optional, Union

from .dclass import StatusElementNotification
from .notification_queue import NotificationQueue
from .constants import STATUS_ELEMENTS, NotificationType
from .utils import get_status_element


def toast_stn(*args: Any, **kwargs: Any) -> None:
    """Display a toast notification."""
    return get_status_element(NotificationType.TOAST)(*args, **kwargs)


def balloons_stn(*args: Any, **kwargs: Any) -> None:
    """Display a balloons notification."""
    return get_status_element(NotificationType.BALLOONS)(*args, **kwargs)


def snow_stn(*args: Any, **kwargs: Any) -> None:
    """Display a snow notification."""
    return get_status_element(NotificationType.SNOW)(*args, **kwargs)


def success_stn(*args: Any, **kwargs: Any) -> None:
    """Display a success notification."""
    return get_status_element(NotificationType.SUCCESS)(*args, **kwargs)


def info_stn(*args: Any, **kwargs: Any) -> None:
    """Display an info notification."""
    return get_status_element(NotificationType.INFO)(*args, **kwargs)


def error_stn(*args: Any, **kwargs: Any) -> None:
    """Display an error notification."""
    return get_status_element(NotificationType.ERROR)(*args, **kwargs)


def warning_stn(*args: Any, **kwargs: Any) -> None:
    """Display a warning notification."""
    return get_status_element(NotificationType.WARNING)(*args, **kwargs)


def exception_stn(*args: Any, **kwargs: Any) -> None:
    """Display an exception notification."""
    return get_status_element(NotificationType.EXCEPTION)(*args, **kwargs)


NotificationStrTypes = Literal[
    "toast", "balloons", "snow", "success", "info", "error", "warning", "exception"
]


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

    get_status_element(notification_type).create_notification(*args, **kwargs)


def _resolve_types(
    notification_type: Optional[
        Union[NotificationStrTypes, Iterable[NotificationStrTypes]]
    ],
) -> List[NotificationType]:
    if notification_type is None:
        return list(STATUS_ELEMENTS.keys())
    if isinstance(notification_type, str):
        return [notification_type]
    return list(notification_type)


def notify(
    remove: bool = True,
    notification_type: Optional[
        Union[NotificationStrTypes, Iterable[NotificationStrTypes]]
    ] = None,
) -> None:
    """
    Display queued notifications.
    """
    types = _resolve_types(notification_type)
    for nt in types:
        get_status_element(nt).notify(remove=remove)


def get_notifications(
    notification_type: Optional[
        Union[NotificationStrTypes, Iterable[NotificationStrTypes]]
    ] = None,
) -> List[StatusElementNotification]:
    """
    Retrieve all notifications for a specific type.
    If no type is specified, retrieves all notifications.
    """
    types = _resolve_types(notification_type)
    notifications = []
    for nt in types:
        notifications.extend(get_status_element(nt).notifications.get_all())

    return notifications


def clear_notifications(
    notification_type: Optional[
        Union[NotificationStrTypes, Iterable[NotificationStrTypes]]
    ] = None,
) -> None:
    """
    Clear notifications for a specific type.
    If no type is specified, clears all notifications.
    """
    types = _resolve_types(notification_type)
    for nt in types:
        get_status_element(nt).notifications.clear()


def get_notification_queue(
    notification_type: NotificationStrTypes,
) -> NotificationQueue:
    """
    Retrieve notifications for a specific type.
    """
    return get_status_element(notification_type).notifications

def has_notifications(
    notification_type: Optional[
        Union[NotificationStrTypes, Iterable[NotificationStrTypes]]
    ] = None,
) -> bool:
    """
    Check if there are any notifications of a specific type.
    If no type is specified, checks for any notifications.
    """
    types = _resolve_types(notification_type)
    for nt in types:
        if not get_status_element(nt).notifications.is_empty():
            return True
    return False


def remove_notification(
    notification: StatusElementNotification,
) -> None:
    """
    Remove a specific notification from the queue.
    """
    get_status_element(notification.name).notifications.remove(notification)