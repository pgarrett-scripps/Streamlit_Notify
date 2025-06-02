"""
Module for queue management of Streamlit notifications.
"""

from typing import Optional
import threading

import streamlit as st

from .dclass import StatusElementNotification


class StreamlitNotificationQueue:
    """
    A thread-safe queue for Streamlit notifications stored in session state.
    """

    def __init__(self, queue_name: str) -> None:
        self.queue_name = queue_name
        self.lock = threading.Lock()
        self._ensure_queue()

    def _ensure_queue(self) -> None:
        """Ensure the queue exists in session state."""
        if self.queue_name not in st.session_state:
            st.session_state[self.queue_name] = []

    def add(self, item: StatusElementNotification) -> None:
        """Add an item to the queue in session state.

        Items are sorted by priority (highest first) after addition.
        """
        with self.lock:
            self._ensure_queue()
            st.session_state[self.queue_name].append(item)
            # Sort by priority (highest first)
            st.session_state[self.queue_name].sort(key=lambda x: -x.priority)

    def get_all(self) -> list[StatusElementNotification]:
        """Get the current queue from session state."""
        with self.lock:
            self._ensure_queue()
            return st.session_state[self.queue_name]

    def clear(self) -> None:
        """Clear the queue in session state."""
        with self.lock:
            self._ensure_queue()
            st.session_state[self.queue_name] = []

    def pop(self) -> Optional[StatusElementNotification]:
        """Pop an item from the queue in session state."""
        with self.lock:
            self._ensure_queue()
            if st.session_state[self.queue_name]:
                return st.session_state[self.queue_name].pop(0)
            return None

    def get(self) -> Optional[StatusElementNotification]:
        """Get the current queue for the widget from session state."""
        with self.lock:
            self._ensure_queue()
            if st.session_state[self.queue_name]:
                return st.session_state[self.queue_name][0]
            return None

    def __len__(self) -> int:
        """Get the size of the queue."""
        with self.lock:
            self._ensure_queue()
            return len(st.session_state[self.queue_name])


class NotificationQueue:
    """
    A notification queue for Streamlit Status Elements.
    """

    def __init__(self, queue_name: str) -> None:
        self.queue_name = queue_name
        self.queue = StreamlitNotificationQueue(queue_name)

    def notify(self, remove: bool = True) -> None:
        """Display all queued notifications for the widget."""
        if remove:
            while len(self.queue) > 0:
                notification = self.queue.pop()
                notification.notify()
        else:
            for notification in self.queue.get_all():
                notification.notify()

    def has_notifications(self) -> bool:
        """Check if there are any notifications in the queue."""
        return len(self.queue) > 0

    def clear_notifications(self) -> None:
        """Clear the notification queue."""
        self.queue.clear()

    def pop_notification(self) -> StatusElementNotification:
        """Pop a notification from the queue."""
        return self.queue.pop()

    def add_notification(self, notification: StatusElementNotification) -> None:
        """Add a notification to the queue."""
        self.queue.add(notification)

    def get_notifications(self) -> list[StatusElementNotification]:
        """Get all notifications in the queue."""
        return self.queue.get_all()
