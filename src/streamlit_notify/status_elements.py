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
    
    def __name__(self) -> str:
        """
        Get the name of the wrapped widget function.

        Returns
        -------
        str
            The name of the base widget function
        """
        return self.base_widget.__name__
    
    def __repr__(self) -> str:
        """
        Get a string representation of the RerunnableStatusElement.

        Returns
        -------
        str
            A string representation of the RerunnableStatusElement
        """
        return f"RerunnableStatusElement({self.base_widget.__name__})"
    
    def __str__(self) -> str:
        """
        Get a string representation of the RerunnableStatusElement.

        Returns
        -------
        str
            A string representation of the RerunnableStatusElement
        """
        return f"RerunnableStatusElement({self.base_widget.__name__})"
    
    def __eq__(self, other: Any) -> bool:
        """
        Check if this RerunnableStatusElement is equal to another object.

        Parameters
        ----------
        other : Any
            The object to compare against

        Returns
        -------
        bool
            True if the other object is a RerunnableStatusElement with the same base widget, False otherwise
        """
        if not isinstance(other, RerunnableStatusElement):
            return False
        return self.base_widget == other.base_widget
    
    def __hash__(self) -> int:
        """
        Get the hash of the RerunnableStatusElement.

        Returns
        -------
        int
            The hash of the base widget function
        """
        return hash(self.base_widget)
    

    def __len__(self) -> int:
        """
        Get the number of notifications in the queue.

        Returns
        -------
        int
            The number of notifications in the queue
        """
        return len(self.queue)
    
    
