"""Utility functions for Streamlit Notify."""

from typing import Union

from .status_element_types import STATUS_ELEMENTS, NotificationType
from .status_elements import RerunnableStatusElement


def get_status_element(
    notification_type: Union[NotificationType, str],
) -> RerunnableStatusElement:
    """Get the Streamlit status element corresponding to the notification type."""
    try:
        if isinstance(notification_type, NotificationType):
            return STATUS_ELEMENTS[notification_type.value]
        return STATUS_ELEMENTS[notification_type]
    except KeyError as err:
        raise KeyError(
            f"Invalid notification type: {notification_type}. "
            f"Must be one of {list(STATUS_ELEMENTS.keys())}."
        ) from err
