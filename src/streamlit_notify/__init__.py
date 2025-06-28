"""
Initialization module for the st_notify package.
"""

__version__ = "0.2.1"

from typing import Any
import streamlit as st
from .status_elements import RerunnableStatusElement
from .functional import (
    create_notification,
    notify,
    get_notifications,
    clear_notifications,
    get_notification_queue,
    has_notifications,
)
from .notification_queue import NotificationQueue  # type: ignore
from .dclass import StatusElementNotification  # type: ignore
from .constants import (
    STATUS_ELEMENTS,
    NotificationType,
    toast,
    balloons,
    snow,
    success,
    info,
    error,
    warning,
    exception,
)  # type: ignore

from .utils import get_status_element  # type: ignore


def init_session_state() -> None:
    """
    Initialize session state for all notification elements.
    This ensures that the notification queues are set up in the session state.
    """
    for name, element in STATUS_ELEMENTS.items():
        element.setup_queue()


init_session_state()


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
