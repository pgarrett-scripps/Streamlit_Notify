"""
Objects for Streamlit notifications.
"""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class StatusElementNotification:
    """
    A notification that can be displayed by a Streamlit widget.

    Parameters
    ----------
    base_widget : Callable
        The original Streamlit widget function to use for display
    args : OrderedDict[str, Any]
        Arguments to pass to the base widget when displayed
    priority : int, optional
        Priority of the notification. Higher values indicate higher priority.
        Defaults to 0.
    data : Any, optional
        Additional data to store with the notification. Defaults to None.

    Attributes
    ----------
    base_widget : Callable
        The original Streamlit widget function to use for display
    args : OrderedDict[str, Any]
        Arguments to pass to the base widget when displayed
    priority : int
        Priority of the notification. Higher values indicate higher priority.
    data : Any
        Additional data stored with the notification.
    """

    base_widget: Callable
    args: OrderedDict[str, Any]
    priority: int = 0
    data: Any = None

    def notify(self) -> None:
        """
        Display the notification using the base widget.
        """
        self.base_widget(**self.args)

    @property
    def name(self) -> str:
        """
        Get the name of the base widget.

        Returns
        -------
        str
            The name of the base widget.
        """
        return self.base_widget.__name__

    def __repr__(self) -> str:
        """
        String representation of the notification.

        Returns
        -------
        str
            The string representation of the notification.
        """
        return (
            f"WidgetNotification(base_widget={self.base_widget.__name__}, args={self.args}, "
            f"priority={self.priority}, data={self.data})"
        )
