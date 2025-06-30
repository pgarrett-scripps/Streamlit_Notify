from streamlit.testing.v1 import AppTest
import pytest


def app_script_get_notifications():
    """App script to test get_notifications function"""
    import streamlit as st
    import streamlit_notify as stn

    stn.init_session_state()

    snotification = stn.create_notification(
        "This is a created notification",
        notification_type="success",
        priority=1,
    )

    if st.button("Add Notifications", key="add_btn"):
        stn.success("Success notification")
        stn.error("Error notification")
        stn.warning("Warning notification")
        stn.info("Info notification")

    if st.button("Notify", key="notify_btn"):
        stn.notify(remove=True)

    if st.button("Get Notifications", key="get_notifications_btn"):
        notifications = stn.get_notifications()
        st.text(f"{len(notifications)}")

        notifications = stn.get_notifications(notification_type=["success"])
        st.text(f"{len(notifications)}")

        notifications = stn.get_notifications(notification_type=["success", "error"])
        st.text(f"{len(notifications)}")

    if st.button("Clear success notifications", key="clear_success_btn"):
        stn.clear_notifications(notification_type=["success"])

    if st.button("Clear all notifications", key="clear_all_btn"):
        stn.clear_notifications()

    if st.button("Create and add notifications", key="create_add_btn"):
        stn.add_notifications(snotification)

    if st.button("Remove success notifications", key="remove_success_btn"):
        stn.remove_notifications(snotification)

    if st.button(
        "Clear success and error notifications", key="clear_success_error_btn"
    ):
        stn.clear_notifications(notification_type=["success", "error"])


class TestFunctionalAPI:
    """Tests for get_notifications and clear_notifications functions."""

    def test_get_notifications(self):
        """Test get_notifications without type filter returns all notifications."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # Check that no notifications are displayed initially
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Get all notifications
        at.button(key="get_notifications_btn").click()
        at.run()

        assert at.text[0].body == "4"
        assert at.text[1].body == "1"
        assert at.text[2].body == "2"

    def test_clear_notifications(self):
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # Check that no notifications are displayed initially
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Clear success notifications
        at.button(key="clear_success_btn").click()
        at.run()

        import streamlit_notify as stn

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # Check that no notifications are displayed initially
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Add notifications
        at.button(key="clear_success_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 2
        assert len(at.session_state[stn.warning.session_state_key]) == 2
        assert len(at.session_state[stn.info.session_state_key]) == 2

        # clear_success_error_btn
        at.button(key="clear_success_error_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 2
        assert len(at.session_state[stn.info.session_state_key]) == 2

        # clear_all_btn
        at.button(key="clear_all_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

    def test_has_notifications(self):
        """Test has_notifications function."""

        def app_script_has_notifications():
            import streamlit as st
            import streamlit_notify as stn
            from streamlit_notify.functional import has_notifications

            stn.init_session_state()

            if st.button("Check has notifications", key="check_btn"):
                result = has_notifications()
                st.text(f"has_any: {result}")

                result = has_notifications(notification_type="success")
                st.text(f"has_success: {result}")

            if st.button("Add notifications", key="add_btn"):
                stn.success("Success message")
                stn.error("Error message")

        at = AppTest.from_function(app_script_has_notifications, default_timeout=10)
        at.run()

        # Check initially no notifications
        at.button(key="check_btn").click()
        at.run()

        assert at.text[0].body == "has_any: False"
        assert at.text[1].body == "has_success: False"

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check now has notifications
        at.button(key="check_btn").click()
        at.run()

        assert at.text[0].body == "has_any: True"
        assert at.text[1].body == "has_success: True"

    def test_get_notification_queue(self):
        """Test get_notification_queue function."""

        def app_script_get_queue():
            import streamlit as st
            import streamlit_notify as stn
            from streamlit_notify.functional import get_notification_queue

            stn.init_session_state()

            if st.button("Check queue", key="check_btn"):
                queue = get_notification_queue("success")
                st.text(f"queue_empty: {queue.is_empty()}")
                st.text(f"queue_length: {len(queue.get_all())}")

            if st.button("Add notification", key="add_btn"):
                stn.success("Success message")

        at = AppTest.from_function(app_script_get_queue, default_timeout=10)
        at.run()

        # Check empty queue initially
        at.button(key="check_btn").click()
        at.run()

        assert at.text[0].body == "queue_empty: True"
        assert at.text[1].body == "queue_length: 0"

        # Add notification
        at.button(key="add_btn").click()
        at.run()

        # Check queue has notification
        at.button(key="check_btn").click()
        at.run()

        assert at.text[0].body == "queue_empty: False"
        assert at.text[1].body == "queue_length: 1"

    def test_notification_functions(self):
        """Test individual notification functions like success_stn, error_stn, etc."""

        def app_script_individual_functions():
            import streamlit as st
            import streamlit_notify as stn
            from streamlit_notify.functional import (
                success_stn,
                error_stn,
                warning_stn,
                info_stn,
            )

            stn.init_session_state()

            if st.button("Add with functions", key="add_btn"):
                success_stn("Success message")
                error_stn("Error message")
                warning_stn("Warning message")
                info_stn("Info message")

            if st.button("Check counts", key="check_btn"):
                success_notifications = stn.get_notifications(
                    notification_type=["success"]
                )
                error_notifications = stn.get_notifications(notification_type=["error"])
                warning_notifications = stn.get_notifications(
                    notification_type=["warning"]
                )
                info_notifications = stn.get_notifications(notification_type=["info"])

                st.text(f"success: {len(success_notifications)}")
                st.text(f"error: {len(error_notifications)}")
                st.text(f"warning: {len(warning_notifications)}")
                st.text(f"info: {len(info_notifications)}")

        at = AppTest.from_function(app_script_individual_functions, default_timeout=10)
        at.run()

        # Add notifications using individual functions
        at.button(key="add_btn").click()
        at.run()

        # Check they were created
        at.button(key="check_btn").click()
        at.run()

        assert at.text[0].body == "success: 1"
        assert at.text[1].body == "error: 1"
        assert at.text[2].body == "warning: 1"
        assert at.text[3].body == "info: 1"

    def test_create_notification(self):
        """Test create_notification function."""

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # create a notification
        at.button(key="create_add_btn").click()
        at.run()

        # see size of the queue
        at.button(key="get_notifications_btn").click()
        at.run()

        # Check that the created notification is in the queue
        assert at.text[1].body == "1"

        # remove the created notification
        at.button(key="remove_success_btn").click()
        at.run()

        # Check that the created notification is removed
        at.button(key="get_notifications_btn").click()
        at.run()

        # Check that the queue is empty
        assert at.text[1].body == "0"

    def test_add_multiple_notifications(self):
        """Test adding multiple notifications at once."""

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # create a notification 3x
        at.button(key="create_add_btn").click()
        at.run()
        at.button(key="create_add_btn").click()
        at.run()
        at.button(key="create_add_btn").click()
        at.run()

        # see size of the queue
        at.button(key="get_notifications_btn").click()
        at.run()

        # Check that the created notification is in the queue
        assert at.text[1].body == "3"

        # remove the created notification
        at.button(key="remove_success_btn").click()
        at.run()

        # Check that the created notification is removed
        at.button(key="get_notifications_btn").click()
        at.run()

        # Check that the queue is 2
        assert at.text[1].body == "2"
