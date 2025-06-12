
from typing import Any, Literal, Optional
from . import STATUS_ELEMENTS

def toast_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a toast notification.
    """
    return STATUS_ELEMENTS["toast"](*args, **kwargs)

def balloons_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a balloons notification.
    """
    return STATUS_ELEMENTS["balloons"](*args, **kwargs)

def snow_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a snow notification.
    """
    return STATUS_ELEMENTS["snow"](*args, **kwargs)

def success_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a success notification.
    """
    return STATUS_ELEMENTS["success"](*args, **kwargs)

def info_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display an info notification.
    """
    return STATUS_ELEMENTS["info"](*args, **kwargs)

def error_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display an error notification.
    """
    return STATUS_ELEMENTS["error"](*args, **kwargs)

def warning_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display a warning notification.
    """
    return STATUS_ELEMENTS["warning"](*args, **kwargs)

def exception_stn(*args: Any, **kwargs: Any) -> None:
    """
    Display an exception notification.
    """
    return STATUS_ELEMENTS["exception"](*args, **kwargs)

def notify(remove: bool = True, filter: Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']] = None) -> None:
    """
    Display all queued notifications.
    Parameters
    ----------
    remove : bool, optional
        If True, remove notifications after displaying them.
        Defaults to True. If False, notifications will remain in the queue
        for the next rerun cycle.
    filter : Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']], optional
        If specified, only display notifications for the given widget type.
        Defaults to None, which displays all notifications.
    """
    if filter is None:
        for widget in STATUS_ELEMENTS.values():
            widget.notify(remove=remove)

    elif filter in STATUS_ELEMENTS:
        STATUS_ELEMENTS[filter].notify(remove=remove)
    else:
        raise ValueError(f"Invalid filter: {filter}. Must be one of {list(STATUS_ELEMENTS.keys())}.")
    
def has_notifications(filter: Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']] = None) -> bool:
    """
    Check if there are any queued notifications.
    
    Parameters
    ----------
    filter : Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']], optional
        If specified, check for notifications only for the given widget type.
        Defaults to None, which checks all notifications.

    Returns
    -------
    bool
        True if any widget has notifications queued.
    """
    if filter is None:
        return any(widget.has_notifications() for widget in STATUS_ELEMENTS.values())
    
    elif filter in STATUS_ELEMENTS:
        return STATUS_ELEMENTS[filter].has_notifications()
    
    else:
        raise ValueError(f"Invalid filter: {filter}. Must be one of {list(STATUS_ELEMENTS.keys())}.")

def clear_notifications(filter: Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']] = None) -> None:
    """
    Clear all notification queues.
    
    Parameters
    ----------
    filter : Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']], optional
        If specified, clear notifications only for the given widget type.
        Defaults to None, which clears all notifications.
    """
    if filter is None:
        for widget in STATUS_ELEMENTS.values():
            widget.clear_notifications()
    
    elif filter in STATUS_ELEMENTS:
        STATUS_ELEMENTS[filter].clear_notifications()
    
    else:
        raise ValueError(f"Invalid filter: {filter}. Must be one of {list(STATUS_ELEMENTS.keys())}.")
    

def get_notifications(filter: Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']] = None) -> dict[str, list[Any]]:
    """
    Get all notifications from all widgets.
    
    Parameters
    ----------
    filter : Optional[Literal['toast', 'balloons', 'snow', 'success', 'info', 'error', 'warning', 'exception']], optional
        If specified, get notifications only for the given widget type.
        Defaults to None, which gets all notifications.
    Returns
    -------
    dict[str, list[Any]]
        A dictionary mapping widget names to their notification lists.
    """
    if filter is None:
        return {name: widget.get_notifications() for name, widget in STATUS_ELEMENTS.items()}
    
    elif filter in STATUS_ELEMENTS:
        return {filter: STATUS_ELEMENTS[filter].get_notifications()}
    
    else:
        raise ValueError(f"Invalid filter: {filter}. Must be one of {list(STATUS_ELEMENTS.keys())}.")