"""Initialization module for the st_notify package."""

__version__ = "0.3.1"
from typing import TYPE_CHECKING, Any

import streamlit as st

from .functional import (
    add_notifications,
    balloons_stn,
    clear_notifications,
    create_notification,
    error_stn,
    exception_stn,
    get_notification_queue,
    get_notifications,
    has_notifications,
    info_stn,
    notify,
    remove_notifications,
    snow_stn,
    success_stn,
    toast_stn,
    warning_stn,
)
from .notification_dataclass import StatusElementNotification
from .notification_queue import NotificationPriorityQueue
from .status_element_types import (
    STATUS_ELEMENTS,
    NotificationType,
    balloons,
    error,
    exception,
    info,
    snow,
    success,
    toast,
    warning,
)
from .status_elements import RerunnableStatusElement
from .utils import get_status_element

# Explicit __all__ to control what gets exported and reduce type errors
__all__ = [
    "__version__",
    "RerunnableStatusElement",
    "create_notification",
    "notify",
    "get_notifications",
    "clear_notifications",
    "get_notification_queue",
    "has_notifications",
    "remove_notifications",
    "add_notifications",
    "toast_stn",
    "balloons_stn",
    "snow_stn",
    "success_stn",
    "info_stn",
    "error_stn",
    "warning_stn",
    "exception_stn",
    "NotificationPriorityQueue",
    "StatusElementNotification",
    "STATUS_ELEMENTS",
    "NotificationType",
    "toast",
    "balloons",
    "snow",
    "success",
    "info",
    "error",
    "warning",
    "exception",
    "get_status_element",
    "init_session_state",
]


def init_session_state() -> None:
    """Initialize session state for all notification elements."""
    for _, element in STATUS_ELEMENTS.items():
        element.setup_queue()


init_session_state()

if not TYPE_CHECKING:

    def __getattr__(name: str) -> Any:
        """Delegate attribute access to Streamlit if not found in this module.

        This function is not included in type checking to prevent it from
        appearing in stub files.

        Args:
            name: Name of the attribute to get.

        Returns:
            The requested attribute from Streamlit.

        Raises:
            AttributeError: If the attribute is not found in Streamlit.
        """
        try:
            return getattr(st, name)
        except AttributeError as err:
            raise AttributeError(str(err).replace("streamlit", "st_notify")) from err
