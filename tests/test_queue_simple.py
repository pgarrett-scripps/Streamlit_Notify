"""
Simple test class for StreamlitNotificationQueue functionality.
"""

from typing import Any, Dict
import unittest
from unittest.mock import Mock, patch
from collections import OrderedDict

# Import the classes we want to test
from src.streamlit_notify.queue import NotificationQueue
from src.streamlit_notify.dclass import StatusElementNotification


class TestStreamlitNotificationQueue(unittest.TestCase):
    """Test class for StreamlitNotificationQueue."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock st.session_state as a dictionary
        self.mock_session_state: Dict[str, Any] = {}
        
        # Create a mock streamlit module
        self.mock_st = Mock()
        self.mock_st.session_state = self.mock_session_state
        
        # Patch streamlit import in the queue module
        self.patcher = patch('src.streamlit_notify.queue.st', self.mock_st)
        self.patcher.start()
        
        # Set up test queue
        self.queue_name = "test_queue"
        self.queue = NotificationQueue(self.queue_name)
        
        # Create sample notifications for testing
        self.mock_widget1 = Mock()
        self.mock_widget1.__name__ = "test_widget1"
        self.mock_widget2 = Mock()
        self.mock_widget2.__name__ = "test_widget2"
        
        self.notification1 = StatusElementNotification(
            base_widget=self.mock_widget1,
            args=OrderedDict([("message", "Test message 1")]),
            priority=1,
            data="test_data1"
        )
        
        self.notification2 = StatusElementNotification(
            base_widget=self.mock_widget2,
            args=OrderedDict([("message", "Test message 2")]),
            priority=2,
            data="test_data2"
        )
        
        self.notification3 = StatusElementNotification(
            base_widget=self.mock_widget1,
            args=OrderedDict([("message", "Test message 3")]),
            priority=0,
            data="test_data3"
        )

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_queue_initialization(self):
        """Test that queue is properly initialized."""
        self.assertEqual(self.queue.queue_name, self.queue_name)
        self.assertIn(self.queue_name, self.mock_session_state)
        self.assertEqual(self.mock_session_state[self.queue_name], [])

    def test_add_single_notification(self):
        """Test adding a single notification to the queue."""
        self.queue.append(self.notification1)
        
        self.assertEqual(len(self.queue), 1)
        self.assertIn(self.notification1, self.mock_session_state[self.queue_name])

    def test_add_multiple_notifications_priority_sorting(self):
        """Test adding multiple notifications and verify priority sorting."""
        # Add notifications in different order
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification3)  # priority 0
        self.queue.append(self.notification2)  # priority 2
        
        notifications = self.queue.get_all()
        
        # Should be sorted by priority (highest first)
        self.assertEqual(len(notifications), 3)
        self.assertEqual(notifications[0], self.notification2)  # priority 2
        self.assertEqual(notifications[1], self.notification1)  # priority 1
        self.assertEqual(notifications[2], self.notification3)  # priority 0

    def test_remove_notification(self):
        """Test removing a notification from the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        self.assertEqual(len(self.queue), 2)
        
        self.queue.remove(self.notification1)
        
        self.assertEqual(len(self.queue), 1)
        self.assertNotIn(self.notification1, self.mock_session_state[self.queue_name])
        self.assertIn(self.notification2, self.mock_session_state[self.queue_name])

    def test_remove_nonexistent_notification(self):
        """Test removing a notification that doesn't exist in the queue."""
        self.queue.append(self.notification1)
        
        with self.assertRaises(ValueError) as context:
            self.queue.remove(self.notification2)
        
        self.assertIn("not found in queue", str(context.exception))

    def test_get_all_notifications(self):
        """Test getting all notifications from the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        notifications = self.queue.get_all()
        
        self.assertEqual(len(notifications), 2)
        self.assertIsInstance(notifications, list)

    def test_clear_queue(self):
        """Test clearing the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        self.assertEqual(len(self.queue), 2)
        
        self.queue.clear()
        
        self.assertEqual(len(self.queue), 0)
        self.assertEqual(self.mock_session_state[self.queue_name], [])

    def test_pop_notification(self):
        """Test popping a notification from the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        # Should pop the highest priority notification first
        popped = self.queue.pop()
        
        self.assertEqual(popped, self.notification2)  # priority 2
        self.assertEqual(len(self.queue), 1)
        self.assertNotIn(self.notification2, self.mock_session_state[self.queue_name])

    def test_pop_from_empty_queue(self):
        """Test popping from an empty queue."""
        popped = self.queue.pop()
        self.assertIsNone(popped)

    def test_get_notification(self):
        """Test getting a notification without removing it."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        # Should get the highest priority notification
        notification = self.queue.get()
        
        self.assertEqual(notification, self.notification2)  # priority 2
        self.assertEqual(len(self.queue), 2)  # Should not remove it

    def test_get_from_empty_queue(self):
        """Test getting from an empty queue."""
        notification = self.queue.get()
        self.assertIsNone(notification)

    def test_queue_length(self):
        """Test the queue length functionality."""
        self.assertEqual(len(self.queue), 0)
        
        self.queue.append(self.notification1)
        self.assertEqual(len(self.queue), 1)
        
        self.queue.append(self.notification2)
        self.assertEqual(len(self.queue), 2)
        
        self.queue.pop()
        self.assertEqual(len(self.queue), 1)

    def test_extend_notifications(self):
        """Test extending the queue with multiple notifications."""
        notifications = [self.notification1, self.notification2, self.notification3]
        self.queue.extend(notifications)
        
        self.assertEqual(len(self.queue), 3)
        # Should be sorted by priority (highest first)
        all_notifications = self.queue.get_all()
        self.assertEqual(all_notifications[0], self.notification2)  # priority 2
        self.assertEqual(all_notifications[1], self.notification1)  # priority 1
        self.assertEqual(all_notifications[2], self.notification3)  # priority 0

    def test_contains_notification(self):
        """Test checking if queue contains a notification."""
        self.assertFalse(self.notification1 in self.queue)
        
        self.queue.append(self.notification1)
        
        self.assertTrue(self.notification1 in self.queue)
        self.assertFalse(self.notification2 in self.queue)

    def test_queue_indexing(self):
        """Test accessing notifications by index."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        # Should be sorted by priority
        self.assertEqual(self.queue[0], self.notification2)  # priority 2
        self.assertEqual(self.queue[1], self.notification1)  # priority 1

    def test_queue_indexing_out_of_range(self):
        """Test accessing notifications with invalid index."""
        self.queue.append(self.notification1)
        
        with self.assertRaises(IndexError):
            _ = self.queue[5]

    def test_remove_by_index(self):
        """Test removing notification by index."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        self.assertEqual(len(self.queue), 2)
        
        self.queue.remove(0)  # Remove first item (highest priority)
        
        self.assertEqual(len(self.queue), 1)
        self.assertEqual(self.queue[0], self.notification1)  # Should be notification1 left

    def test_queue_iteration(self):
        """Test iterating over the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        
        notifications = list(self.queue)
        
        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0], self.notification2)  # priority 2
        self.assertEqual(notifications[1], self.notification1)  # priority 1


class TestNotificationQueue(unittest.TestCase):
    """Test class for NotificationQueue wrapper."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock st.session_state as a dictionary
        self.mock_session_state: Dict[str, Any] = {}
        
        # Create a mock streamlit module
        self.mock_st = Mock()
        self.mock_st.session_state = self.mock_session_state
        
        # Patch streamlit import in the queue module
        self.patcher = patch('src.streamlit_notify.queue.st', self.mock_st)
        self.patcher.start()
        
        # Set up test queue
        self.queue_name = "test_notification_queue"
        self.notification_queue = NotificationQueue(self.queue_name)
        
        # Create sample notification
        self.mock_widget = Mock()
        self.mock_widget.__name__ = "test_widget"
        
        self.notification = StatusElementNotification(
            base_widget=self.mock_widget,
            args=OrderedDict([("message", "Test message")]),
            priority=1,
            data="test_data"
        )

    def tearDown(self):
        """Clean up after each test method."""
        self.patcher.stop()

    def test_notification_queue_initialization(self):
        """Test that NotificationQueue is properly initialized."""
        self.assertEqual(self.notification_queue.queue_name, self.queue_name)
        self.assertIsInstance(self.notification_queue, NotificationQueue)

    def test_add_notification(self):
        """Test adding a notification through the wrapper."""
        self.notification_queue.append(self.notification)
        
        self.assertTrue(self.notification_queue.has_items())
        self.assertEqual(len(self.notification_queue), 1)

    def test_has_items(self):
        """Test checking if queue has notifications."""
        self.assertFalse(self.notification_queue.has_items())
        
        self.notification_queue.append(self.notification)
        
        self.assertTrue(self.notification_queue.has_items())

    def test_clear_notifications(self):
        """Test clearing notifications."""
        self.notification_queue.append(self.notification)
        self.assertTrue(self.notification_queue.has_items())
        
        self.notification_queue.clear()
        
        self.assertFalse(self.notification_queue.has_items())

    def test_pop_notification(self):
        """Test popping a single notification."""
        self.notification_queue.append(self.notification)
        
        popped = self.notification_queue.pop()
        
        self.assertEqual(popped, self.notification)
        self.assertFalse(self.notification_queue.has_items())

    def test_get_notifications(self):
        """Test getting all notifications."""
        self.notification_queue.append(self.notification)
        
        notifications = self.notification_queue.get_all()
        
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0], self.notification)
        # Should not remove notifications
        self.assertTrue(self.notification_queue.has_items())

    def test_queue_size(self):
        """Test getting queue size."""
        self.assertEqual(self.notification_queue.size(), 0)
        
        self.notification_queue.append(self.notification)
        
        self.assertEqual(self.notification_queue.size(), 1)

    def test_queue_boolean_representation(self):
        """Test boolean representation of queue."""
        self.assertFalse(bool(self.notification_queue))
        
        self.notification_queue.append(self.notification)
        
        self.assertTrue(bool(self.notification_queue))

    def test_get_notification_without_removing(self):
        """Test getting a notification without removing it."""
        self.notification_queue.append(self.notification)
        
        retrieved = self.notification_queue.get()
        
        self.assertEqual(retrieved, self.notification)
        self.assertTrue(self.notification_queue.has_items())  # Should still have items

    def test_get_from_empty_queue_wrapper(self):
        """Test getting from empty queue."""
        retrieved = self.notification_queue.get()
        
        self.assertIsNone(retrieved)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
