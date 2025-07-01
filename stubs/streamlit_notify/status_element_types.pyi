from .status_elements import RerunnableStatusElement as RerunnableStatusElement
from _typeshed import Incomplete
from enum import Enum

toast: Incomplete
balloons: Incomplete
snow: Incomplete
success: Incomplete
info: Incomplete
error: Incomplete
warning: Incomplete
exception: Incomplete

class NotificationType(Enum):
    TOAST = 'toast'
    BALLOONS = 'balloons'
    SNOW = 'snow'
    SUCCESS = 'success'
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'
    EXCEPTION = 'exception'

STATUS_ELEMENTS: Incomplete
