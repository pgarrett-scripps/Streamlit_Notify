from .status_element_types import NotificationType as NotificationType, STATUS_ELEMENTS as STATUS_ELEMENTS
from .status_elements import RerunnableStatusElement as RerunnableStatusElement

def get_status_element(notification_type: NotificationType | str) -> RerunnableStatusElement: ...
