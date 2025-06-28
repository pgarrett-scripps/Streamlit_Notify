from typing import Union
from build.lib.streamlit_notify import STATUS_ELEMENTS
from streamlit_notify.constants import NotificationType
from streamlit_notify.status_elements import RerunnableStatusElement


def get_status_element(
    notification_type: Union[NotificationType, str],
) -> RerunnableStatusElement:
    try:
        if isinstance(notification_type, NotificationType):
            return STATUS_ELEMENTS[notification_type.value]
        return STATUS_ELEMENTS[notification_type]
    except KeyError as e:
        raise KeyError(
            f"Invalid notification type: {notification_type}. Must be one of {list(STATUS_ELEMENTS.keys())}."
        ) from e
