"""
Queue management for Streamlit notifications.
"""

from typing import Iterable, List, Optional, Union

import streamlit as st

from .dclass import StatusElementNotification


def _sort_func(x: StatusElementNotification) -> int:
    """Sort notifications by priority (highest first)."""
    return -x.priority


class NotificationQueue:
    """
    A queue for managing Streamlit notifications.
    """

    def __init__(self, queue_name: str) -> None:
        """Initialize the queue."""
        self.queue_name = queue_name
        self._ensure_queue()

    @property
    def queue(self) -> List[StatusElementNotification]:
        """Get the current queue."""
        self._ensure_queue()
        return st.session_state[self.queue_name]

    def _ensure_queue(self) -> None:
        """Ensure the queue exists in session state."""
        if self.queue_name not in st.session_state:
            st.session_state[self.queue_name] = []

    def has_items(self) -> bool:
        """Check if the queue has items."""
        return len(self) > 0

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self) == 0

    def append(self, item: StatusElementNotification) -> None:
        """Add an item to the queue."""
        self.queue.append(item)
        self.queue.sort(key=_sort_func)

    def extend(self, items: Iterable[StatusElementNotification]) -> None:
        """Add multiple items to the queue."""
        self.queue.extend(items)
        self.queue.sort(key=_sort_func)

    def remove(self, item: Union[StatusElementNotification, int]) -> None:
        """Remove an item from the queue."""
        if isinstance(item, int):
            _ = self.pop(index=item)
            return

        if item in self.queue:
            self.queue.remove(item)
            return

        raise ValueError(f"Item: {item} not found in queue.")

    def contains(self, item: StatusElementNotification) -> bool:
        """Check if an item is in the queue."""
        return item in self.queue

    def get_all(self) -> List[StatusElementNotification]:
        """Get all items in the queue."""
        return self.queue

    def clear(self) -> None:
        """Clear the queue."""
        self.queue.clear()

    def pop(self, index: int = 0) -> Optional[StatusElementNotification]:
        """Pop an item from the queue."""
        if self.queue:
            return self.queue.pop(index)
        return None

    def get(self, index: int = 0) -> Optional[StatusElementNotification]:
        """Get an item from the queue without removing it."""
        if self.queue:
            return self.queue[index]
        return None

    def size(self) -> int:
        """Get the size of the queue."""
        return len(self)

    def __len__(self) -> int:
        """Get the size of the queue."""
        return len(self.queue)

    def __repr__(self) -> str:
        """String representation of the queue."""
        return f"NotificationQueue(name={self.queue_name}, items={len(self.queue)})"

    def __str__(self) -> str:
        """String representation of the queue."""
        return f"NotificationQueue({self.queue_name}, {list(self.queue)})"

    def __bool__(self) -> bool:
        """Boolean representation of the queue."""
        return len(self) > 0

    def __contains__(self, item: StatusElementNotification) -> bool:
        """Check if an item is in the queue."""
        return self.contains(item)

    def __getitem__(self, index: int) -> StatusElementNotification:
        """Get an item by index."""
        item = self.get(index=index)
        if item is None:
            raise IndexError("Index out of range")
        return item

    def __setitem__(self, index: int, value: StatusElementNotification) -> None:
        """Set an item by index."""
        self.queue[index] = value

    def __delitem__(self, index: int) -> None:
        """Delete an item by index."""
        del self.queue[index]

    def __hash__(self) -> int:
        """Hash of the queue based on its name."""
        return hash(self.queue_name)

    def __eq__(self, other: object) -> bool:
        """Check if this queue is equal to another."""
        if not isinstance(other, NotificationQueue):
            return False
        if self.queue_name != other.queue_name:
            return False
        if self.get_all() != other.get_all():
            return False
        return True

    def __ne__(self, other: object) -> bool:
        """Check if this queue is not equal to another."""
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        """Check if this queue is less than another."""
        if not isinstance(other, NotificationQueue):
            return NotImplemented
        return self.size() < other.size()

    def __iter__(self) -> Iterable[StatusElementNotification]:
        """Iterate over the notifications in the queue."""
        yield from self.queue

    def __reversed__(self) -> Iterable[StatusElementNotification]:
        """Iterate over the notifications in reverse order."""
        yield from reversed(self.queue)

    def __copy__(self):
        """Create a shallow copy of the queue."""
        new_queue = NotificationQueue(self.queue_name)
        new_queue.extend(self.get_all())
        return new_queue
