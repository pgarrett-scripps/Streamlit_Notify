"""
Initialization module for the st_notify package.
"""

__version__ = "0.2.0"

from typing import Any
import streamlit as st
from .status_elements import RerunnableStatusElement
from .queue import NotificationQueue  # type: ignore
from .dclass import StatusElementNotification  # type: ignore

# Define notification widgets
toast = RerunnableStatusElement(st.toast)
balloons = RerunnableStatusElement(st.balloons)
snow = RerunnableStatusElement(st.snow)
success = RerunnableStatusElement(st.success)
info = RerunnableStatusElement(st.info)
error = RerunnableStatusElement(st.error)
warning = RerunnableStatusElement(st.warning)
exception = RerunnableStatusElement(st.exception)

STATUS_ELEMENTS = {
    "toast": toast,
    "balloons": balloons,
    "snow": snow,
    "success": success,
    "info": info,
    "error": error,
    "warning": warning,
    "exception": exception,
}


def notify_all(remove: bool = True) -> None:
    """
    Display all queued notifications.

    Parameters:
        remove (bool): If True, remove notifications after displaying. Defaults to True.
    """
    for widget in STATUS_ELEMENTS.values():
        widget.notify(remove=remove)


def has_any_notifications() -> bool:
    """
    Check if there are any queued notifications.

    Returns:
        bool: True if any widget has notifications queued.
    """
    return any(len(widget.notifications) > 0 for widget in STATUS_ELEMENTS.values())


def clear_all_notifications() -> None:
    """Clear all notification queues."""
    for widget in STATUS_ELEMENTS.values():
        widget.notifications.clear()


def get_all_notifications() -> dict[str, list[Any]]:
    """
    Get all notifications from all widgets.

    Returns:
        dict[str, list[Any]]: A dictionary mapping widget names to their notification lists.
    """
    return {
        name: widget.notifications.get_all() for name, widget in STATUS_ELEMENTS.items()
    }


def __getattr__(name: str) -> Any:
    """
    Delegate attribute access to Streamlit if not found in this module.

    Parameters:
        name (str): Name of the attribute to get.

    Returns:
        Any: The requested attribute from Streamlit.

    Raises:
        AttributeError: If the attribute is not found in Streamlit.
    """
    try:
        return getattr(st, name)
    except AttributeError as err:
        raise AttributeError(str(err).replace("streamlit", "st_notify")) from err
