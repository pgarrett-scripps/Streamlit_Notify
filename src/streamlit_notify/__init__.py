"""
Initialization module for the st_notify package.
"""

__version__ = "0.1.1"

from typing import Any, Optional

import streamlit as st

from .status_elements import RerunnableStatusElement
from .queue import NotificationQueue
from .dclass import StatusElementNotification


toast = RerunnableStatusElement(st.toast)
balloons = RerunnableStatusElement(st.balloons)
snow = RerunnableStatusElement(st.snow)
success = RerunnableStatusElement(st.success)
info = RerunnableStatusElement(st.info)
error = RerunnableStatusElement(st.error)
warning = RerunnableStatusElement(st.warning)
exception = RerunnableStatusElement(st.exception)

status_elements = {
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

    Parameters
    ----------
    remove : bool, optional
        If True, remove notifications after displaying them.
        Defaults to True. If False, notifications will remain in the queue
        for the next rerun cycle.
    """
    for widget in status_elements.values():
        widget.notify(remove=remove)


def has_any_notifications() -> bool:
    """
    Check if there are any queued notifications.

    Returns
    -------
    bool
        True if any widget has notifications queued.
    """
    return any(widget.has_notifications() for widget in status_elements.values())


def clear_all_notifications() -> None:
    """
    Clear all notification queues.
    """
    for widget in status_elements.values():
        widget.clear_notifications()


def get_all_notifications() -> dict[str, list[Any]]:
    """
    Get all notifications from all widgets.

    Returns
    -------
    dict[str, list[Any]]
        A dictionary mapping widget names to their respective notification lists.
    """
    return {
        name: list(widget.get_notifications())
        for name, widget in status_elements.items()
    }


def __getattr__(name: str) -> Any:
    """
    Delegate attribute access to streamlit if not found in this module.

    Parameters
    ----------
    name : str
        Name of the attribute to get

    Returns
    -------
    Any
        The requested attribute from streamlit

    Raises
    ------
    AttributeError
        If the attribute is not found in streamlit
    """
    try:
        return getattr(st, name)
    except AttributeError as err:
        raise AttributeError(str(err).replace("streamlit", "st_notify")) from err
