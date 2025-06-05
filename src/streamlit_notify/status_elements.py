"""
Widgets that are aware of URL parameters.
"""

import inspect
from typing import Any, Callable

from .queue import NotificationQueue
from .dclass import StatusElementNotification


class RerunnableStatusElement(NotificationQueue):
    """
    A wrapper class that adds notification queueing to Streamlit widgets.

    This class wraps standard Streamlit widgets to enable notifications to be
    queued and displayed during the next rerun cycle.

    Parameters
    ----------
    base_widget : Callable
        The original Streamlit widget function to wrap

    Attributes
    ----------
    base_widget : Callable
        The original Streamlit widget function being wrapped
    """

    def __init__(self, base_widget: Callable) -> None:
        """
        Initialize a new RerunnableStatusElement.

        Parameters
        ----------
        base_widget : Callable
            The original Streamlit widget function to wrap
        """
        self.base_widget = base_widget
        super().__init__(f"ST_NOTIFY_{base_widget.__name__.upper()}_QUEUE")

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Create and add a notification to the queue.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the base widget
        **kwargs : Any
            Keyword arguments to pass to the base widget
        """
        notification = self.create_notification(*args, **kwargs)
        self.add_notification(notification)

    def create_notification(
        self, *args: Any, **kwargs: Any
    ) -> StatusElementNotification:
        """
        Create a notification without adding it to the queue.

        Parameters
        ----------
        *args : Any
            Positional arguments to pass to the base widget
        **kwargs : Any
            Keyword arguments to pass to the base widget

        Returns
        -------
        StatusElementNotification
            A notification for the base widget with the given arguments
        """

        # Extract priority if provided, otherwise default to 0
        priority = kwargs.pop("priority", 0) if "priority" in kwargs else 0
        data = kwargs.pop("data", None) if "data" in kwargs else None

        signature = inspect.signature(self.base_widget)
        bound_args = signature.bind_partial(*args, **kwargs)

        return StatusElementNotification(
            base_widget=self.base_widget,
            args=bound_args.arguments,
            priority=priority,
            data=data,
        )
