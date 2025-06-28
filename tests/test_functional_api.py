from streamlit.testing.v1 import AppTest
import pytest


def app_script_get_notifications():
    """App script to test get_notifications function"""
    import streamlit as st
    import streamlit_notify as stn

    stn.init_session_state()

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

        notifications = stn.get_notifications(notification_type=['success'])
        st.text(f"{len(notifications)}")

        notifications = stn.get_notifications(notification_type=['success', 'error'])
        st.text(f"{len(notifications)}")

    if st.button("Clear success notifications", key="clear_success_btn"):
        stn.clear_notifications(notification_type=['success'])

    if st.button("Clear all notifications", key="clear_all_btn"):
        stn.clear_notifications()

    if st.button("Clear success and error notifications", key="clear_success_error_btn"):
        stn.clear_notifications(notification_type=['success', 'error'])



class TestFunctionalAPI:
    """Tests for get_notifications and clear_notifications functions."""

    def test_get_notifications(self):
        """Test get_notifications without type filter returns all notifications."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_get_notifications, default_timeout=10)
        at.run()

        # Check that no notifications are displayed initially
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
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
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
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
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Add notifications
        at.button(key="clear_success_btn").click()
        at.run()


        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Add notifications
        at.button(key="add_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 2
        assert len(at.session_state[stn.warning.session_state_key]) == 2
        assert len(at.session_state[stn.info.session_state_key]) == 2


        # clear_success_error_btn
        at.button(key="clear_success_error_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 2
        assert len(at.session_state[stn.info.session_state_key]) == 2

        # clear_all_btn
        at.button(key="clear_all_btn").click()
        at.run()

        # Check that notifications are queued but not displayed yet
        assert(len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0
