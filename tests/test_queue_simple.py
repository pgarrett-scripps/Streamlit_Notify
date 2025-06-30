"""
Simple test class for StreamlitNotificationQueue functionality.
"""

from typing import Any, Dict
import unittest
from unittest.mock import Mock, patch
from collections import OrderedDict

# Import the classes we want to test
from streamlit_notify.notification_queue import NotificationQueue
from streamlit_notify.notification_dataclass import StatusElementNotification


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
        self.patcher = patch("streamlit_notify.notification_queue.st", self.mock_st)
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
            data="test_data1",
        )

        self.notification2 = StatusElementNotification(
            base_widget=self.mock_widget2,
            args=OrderedDict([("message", "Test message 2")]),
            priority=2,
            data="test_data2",
        )

        self.notification3 = StatusElementNotification(
            base_widget=self.mock_widget1,
            args=OrderedDict([("message", "Test message 3")]),
            priority=0,
            data="test_data3",
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
        with self.assertRaises(IndexError):
            _ = self.queue.pop()

    def test_get_notification(self):
        """Test getting a notification without removing it."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        # Should get the highest priority notification
        notification = self.queue.get()

        self.assertEqual(notification, self.notification2)  # priority 2
        self.assertEqual(len(self.queue), 2)  # Should not remove it

    def test_get_from_empty_queue(self):
        """Test getting from an empty queue raises IndexError and returns None if handled."""
        with self.assertRaises(IndexError):
            self.queue.get()

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
        self.assertEqual(
            self.queue[0], self.notification1
        )  # Should be notification1 left

    def test_queue_iteration(self):
        """Test iterating over the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        notifications: list[StatusElementNotification] = list(self.queue)

        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0], self.notification2)  # priority 2
        self.assertEqual(notifications[1], self.notification1)  # priority 1

    def test_custom_sort_function(self):
        """Test queue with custom sort function."""

        # Custom sort: lowest priority first
        def custom_sort(x: StatusElementNotification) -> int:
            return x.priority

        custom_queue = NotificationQueue("custom_test_queue", sort_func=custom_sort)

        custom_queue.append(self.notification1)  # priority 1
        custom_queue.append(self.notification2)  # priority 2
        custom_queue.append(self.notification3)  # priority 0

        notifications = custom_queue.get_all()

        # Should be sorted by priority (lowest first with custom function)
        self.assertEqual(notifications[0], self.notification3)  # priority 0
        self.assertEqual(notifications[1], self.notification1)  # priority 1
        self.assertEqual(notifications[2], self.notification2)  # priority 2

    def test_priority_filtering_less_than(self):
        """Test getting notifications with priority less than specified value."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        notifications = self.queue.get_all(priority=2, priority_type="lt")

        self.assertEqual(len(notifications), 2)
        self.assertIn(self.notification1, notifications)
        self.assertIn(self.notification3, notifications)
        self.assertNotIn(self.notification2, notifications)

    def test_priority_filtering_less_than_equal(self):
        """Test getting notifications with priority less than or equal to specified value."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        notifications = self.queue.get_all(priority=1, priority_type="le")

        self.assertEqual(len(notifications), 2)
        self.assertIn(self.notification1, notifications)
        self.assertIn(self.notification3, notifications)
        self.assertNotIn(self.notification2, notifications)

    def test_priority_filtering_greater_than(self):
        """Test getting notifications with priority greater than specified value."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        notifications = self.queue.get_all(priority=0, priority_type="gt")

        self.assertEqual(len(notifications), 2)
        self.assertIn(self.notification1, notifications)
        self.assertIn(self.notification2, notifications)
        self.assertNotIn(self.notification3, notifications)

    def test_priority_filtering_greater_than_equal(self):
        """Test getting notifications with priority greater than or equal to specified value."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        notifications = self.queue.get_all(priority=1, priority_type="ge")

        self.assertEqual(len(notifications), 2)
        self.assertIn(self.notification1, notifications)
        self.assertIn(self.notification2, notifications)
        self.assertNotIn(self.notification3, notifications)

    def test_priority_filtering_equal_to(self):
        """Test getting notifications with priority equal to specified value."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        notifications = self.queue.get_all(priority=1, priority_type="eq")

        self.assertEqual(len(notifications), 1)
        self.assertIn(self.notification1, notifications)

    def test_string_representations(self):
        """Test string representation methods."""
        self.queue.append(self.notification1)

        repr_str = repr(self.queue)
        str_str = str(self.queue)

        self.assertIn("NotificationQueue", repr_str)
        self.assertIn(self.queue_name, repr_str)
        self.assertIn("1", repr_str)  # item count

        self.assertIn("NotificationQueue", str_str)
        self.assertIn(self.queue_name, str_str)
        self.assertIn("1", str_str)  # item count

    def test_queue_equality(self):
        """Test queue equality comparison."""
        queue2 = NotificationQueue("test_queue")

        # Empty queues should be equal
        self.assertEqual(self.queue, queue2)

        # Add same notification to both
        self.queue.append(self.notification1)
        queue2.append(self.notification1)

        self.assertEqual(self.queue, queue2)

    def test_queue_inequality(self):
        """Test queue inequality comparison."""
        queue2 = NotificationQueue("different_queue")

        # Different names should be unequal
        self.assertNotEqual(self.queue, queue2)

        # Test with non-queue object
        self.assertNotEqual(self.queue, "not a queue")

    def test_queue_comparison_less_than(self):
        """Test queue size comparison."""
        queue2 = NotificationQueue("test_queue2")

        # Empty queues should not be less than each other
        self.assertFalse(self.queue < queue2)

        # Add item to queue2
        queue2.append(self.notification1)

        self.assertTrue(self.queue < queue2)
        self.assertFalse(queue2 < self.queue)

    def test_queue_hash(self):
        """Test queue hashing."""
        queue2 = NotificationQueue("test_queue")
        queue3 = NotificationQueue("different_queue")

        # Same name should have same hash
        self.assertEqual(hash(self.queue), hash(queue2))

        # Different name should have different hash
        self.assertNotEqual(hash(self.queue), hash(queue3))

    def test_item_assignment(self):
        """Test assigning items by index."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        # Replace item at index 0
        self.queue[0] = self.notification3

        self.assertEqual(self.queue[-1], self.notification3)

        # Queue should be re-sorted after assignment
        notifications = self.queue.get_all()
        self.assertEqual(notifications[0], self.notification1)  # priority 1
        self.assertEqual(notifications[1], self.notification3)  # priority 0

    def test_item_deletion(self):
        """Test deleting items by index."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        initial_length = len(self.queue)

        del self.queue[0]  # Delete first item (highest priority)

        self.assertEqual(len(self.queue), initial_length - 1)
        self.assertEqual(
            self.queue[0], self.notification1
        )  # Should be notification1 left

    def test_reversed_iteration(self):
        """Test iterating over queue in reverse order."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)
        self.queue.append(self.notification3)

        reversed_notifications = list(reversed(self.queue))
        normal_notifications = list(self.queue)

        self.assertEqual(len(reversed_notifications), 3)
        self.assertEqual(reversed_notifications, list(reversed(normal_notifications)))

    def test_contains_method(self):
        """Test the contains method explicitly."""
        self.assertFalse(self.queue.contains(self.notification1))

        self.queue.append(self.notification1)

        self.assertTrue(self.queue.contains(self.notification1))
        self.assertFalse(self.queue.contains(self.notification2))

    def test_is_empty_method(self):
        """Test the is_empty method."""
        self.assertTrue(self.queue.is_empty())

        self.queue.append(self.notification1)

        self.assertFalse(self.queue.is_empty())

        self.queue.clear()

        self.assertTrue(self.queue.is_empty())

    def test_size_method(self):
        """Test the size method."""
        self.assertEqual(self.queue.size(), 0)

        self.queue.append(self.notification1)
        self.assertEqual(self.queue.size(), 1)

        self.queue.append(self.notification2)
        self.assertEqual(self.queue.size(), 2)

    def test_sort_func_property(self):
        """Test accessing the sort function property."""
        # Default sort function
        sort_func = self.queue.sort_func
        self.assertIsNotNone(sort_func)

        # Test that it sorts correctly (highest priority first)
        self.assertEqual(sort_func(self.notification1), -1)  # -priority
        self.assertEqual(sort_func(self.notification2), -2)  # -priority

    def test_queue_property(self):
        """Test accessing the queue property."""
        queue_list = self.queue.queue
        self.assertIsInstance(queue_list, list)
        self.assertEqual(len(queue_list), 0)

        self.queue.append(self.notification1)

        self.assertEqual(len(queue_list), 1)
        self.assertIn(self.notification1, queue_list)

    def test_shallow_copy(self):
        """Test creating a shallow copy of the queue."""
        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        queue_copy = self.queue.__copy__()

        self.assertEqual(len(queue_copy), len(self.queue))
        self.assertEqual(queue_copy.get_all(), self.queue.get_all())

        # Modify original queue
        self.queue.append(self.notification3)

        # Copy should not be affected
        self.assertEqual(len(queue_copy), len(self.queue))

    def test_deep_copy(self):
        """Test creating a deep copy of the queue."""
        import copy

        self.queue.append(self.notification1)
        self.queue.append(self.notification2)

        queue_copy = copy.deepcopy(self.queue)

        self.assertEqual(len(queue_copy), len(self.queue))
        self.assertEqual(queue_copy.get_all(), self.queue.get_all())

    def test_error_handling_in_priority_methods(self):
        """Test that priority filtering methods handle edge cases properly."""
        self.queue.append(self.notification1)  # priority 1
        self.queue.append(self.notification2)  # priority 2
        self.queue.append(self.notification3)  # priority 0

        # Test edge case: no items match criteria
        empty_results = self.queue.get_all(priority=10, priority_type="gt")
        self.assertEqual(len(empty_results), 0)

        # Test with negative priority
        all_results = self.queue.get_all(priority=-1, priority_type="gt")
        self.assertEqual(len(all_results), 3)


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
        self.patcher = patch("src.streamlit_notify.notification_queue.st", self.mock_st)
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
            data="test_data",
        )

        self.notification_queue.clear()

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
        with self.assertRaises(IndexError):
            _ = self.notification_queue.get()


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2)
