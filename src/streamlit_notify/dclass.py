"""
Streamlit notification objects.
"""

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class StatusElementNotification:
    """
    Represents a notification for a Streamlit widget.
    """

    base_widget: Callable[..., Any]
    args: OrderedDict[str, Any]
    priority: int = 0
    data: Any = None

    def notify(self) -> None:
        """Display the notification using the widget."""
        self.base_widget(**self.args)

    @property
    def name(self) -> str:
        """Get the name of the widget function."""
        return self.base_widget.__name__

    def __repr__(self) -> str:
        """String representation of the notification."""
        return (
            f"WidgetNotification(base_widget={self.base_widget.__name__}, args={self.args}, "
            f"priority={self.priority}, data={self.data})"
        )

    def __name__(self) -> str:
        """Get the name of the notification."""
        return self.name

    def __str__(self) -> str:
        """String representation of the notification."""
        return self.__repr__()

    def __eq__(self, other: object) -> bool:
        """
        Check if this notification is equal to another.
        """
        if not isinstance(other, StatusElementNotification):
            return False
        return (
            self.base_widget == other.base_widget
            and self.args == other.args
            and self.priority == other.priority
            and self.data == other.data
        )
