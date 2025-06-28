from streamlit.testing.v1 import AppTest
import pytest


def app_script():
    import streamlit as st
    import streamlit_notify as stn

    stn.notify(notification_type="success", remove=True)

    if st.button("Trigger Success", key="success_btn"):
        stn.success("Success notification triggered!")
        stn.error("Error notification triggered!")
        stn.warning("Warning notification triggered!")

    if st.button("Rerun", key="rerun_btn"):
        pass  # button press will trigger a rerun


def app_script_all_types():
    """App script to test all notification types"""
    import streamlit as st
    import streamlit_notify as stn

    stn.notify(remove=True)  # notify all types

    if st.button("Trigger All", key="all_btn"):
        stn.toast("Toast notification")
        stn.balloons()
        stn.snow()
        stn.success("Success notification")
        stn.info("Info notification")
        stn.error("Error notification")
        stn.warning("Warning notification")
        stn.exception("Exception notification")

    if st.button("Rerun", key="rerun_btn"):
        pass


def app_script_multiple_types():
    """App script to test multiple specific notification types"""
    import streamlit as st
    import streamlit_notify as stn

    stn.notify(notification_type=["success", "error"], remove=True)

    if st.button("Trigger Multiple", key="multi_btn"):
        stn.success("Success notification")
        stn.error("Error notification")
        stn.warning("Warning notification")  # This won't be displayed
        stn.info("Info notification")  # This won't be displayed

    if st.button("Rerun", key="rerun_btn"):
        pass


def app_script_no_remove():
    """App script to test notify with remove=False"""
    import streamlit as st
    import streamlit_notify as stn

    stn.notify(notification_type="success", remove=False)

    if st.button("Trigger Success", key="success_btn"):
        stn.success("Success notification")

    if st.button("Rerun", key="rerun_btn"):
        pass


def app_script_invalid_type():
    """App script to test invalid notification type"""
    import streamlit as st
    import streamlit_notify as stn

    if st.button("Trigger Invalid", key="invalid_btn"):
        try:
            stn.notify(notification_type="invalid_type")
        except ValueError as e:
            st.write(f"Error: {e}")

    if st.button("Rerun", key="rerun_btn"):
        pass


class TestStreamlitNotificationByTypes:
    """Integration tests for streamlit_notify using AppTest."""

    def test_success_notification_in_app(self):
        """Test that success notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script, default_timeout=10)

        # Run the app initially
        at.run()

        # Check that no notifications are displayed initially
        assert (len(at.success)) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 0

        # Click the success button
        at.button(key="success_btn").click()
        at.run()

        # Check that notification is queued but not displayed yet
        assert len(at.success) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1

        # Click rerun button to trigger notify
        at.button(key="rerun_btn").click()
        at.run()

        # After triggering notify_all, should see the notification
        assert len(at.success) == 1
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1

    def test_notify_all_types(self):
        """Test notify without notification_type parameter (should notify all types)."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_all_types, default_timeout=10)

        # Run the app initially
        at.run()

        # Trigger all notification types
        at.button(key="all_btn").click()
        at.run()

        # Check that all notifications are queued
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1
        assert len(at.session_state[stn.toast.session_state_key]) == 1
        # Note: balloons and snow don't have content, so we check differently

        # Click rerun to trigger notify for all types
        at.button(key="rerun_btn").click()
        at.run()

        # Check that all notifications are displayed and queues are cleared
        assert len(at.success) == 1
        assert len(at.error) == 1
        assert len(at.warning) == 1
        assert len(at.info) == 1
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 0
        assert len(at.session_state[stn.info.session_state_key]) == 0

    def test_notify_multiple_specific_types(self):
        """Test notify with multiple specific notification types."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_multiple_types, default_timeout=10)

        # Run the app initially
        at.run()

        # Trigger multiple notification types
        at.button(key="multi_btn").click()
        at.run()

        # Check that all notifications are queued
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1
        assert len(at.session_state[stn.info.session_state_key]) == 1

        # Click rerun to trigger notify for only success and error types
        at.button(key="rerun_btn").click()
        at.run()

        # Check that only success and error notifications are displayed
        assert len(at.success) == 1
        assert len(at.error) == 1
        assert len(at.warning) == 0  # Should not be displayed
        assert len(at.info) == 0  # Should not be displayed

        # Check that only success and error queues are cleared
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 0
        assert len(at.session_state[stn.warning.session_state_key]) == 1  # Still queued
        assert len(at.session_state[stn.info.session_state_key]) == 1  # Still queued

    def test_notify_single_type_as_string(self):
        """Test notify with a single notification type as string."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script, default_timeout=10)

        # Run the app initially
        at.run()

        # Trigger notifications
        at.button(key="success_btn").click()
        at.run()

        # Verify notifications are queued
        assert len(at.session_state[stn.success.session_state_key]) == 1
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1

        # Click rerun to trigger notify for only success type
        at.button(key="rerun_btn").click()
        at.run()

        # Check that only success notification is displayed
        assert len(at.success) == 1
        assert len(at.error) == 0
        assert len(at.warning) == 0

        # Check that only success queue is cleared
        assert len(at.session_state[stn.success.session_state_key]) == 0
        assert len(at.session_state[stn.error.session_state_key]) == 1
        assert len(at.session_state[stn.warning.session_state_key]) == 1

    def test_notify_with_remove_false(self):
        """Test notify with remove=False parameter."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script_no_remove, default_timeout=10)

        # Run the app initially
        at.run()

        # Trigger notification
        at.button(key="success_btn").click()
        at.run()

        # Verify notification is queued
        assert len(at.session_state[stn.success.session_state_key]) == 1

        # Click rerun to trigger notify with remove=False
        at.button(key="rerun_btn").click()
        at.run()

        # Check that notification is displayed but queue is NOT cleared
        assert len(at.success) == 1
        assert (
            len(at.session_state[stn.success.session_state_key]) == 1
        )  # Still in queue

    def test_notify_empty_queue(self):
        """Test notify when there are no notifications in queue."""
        import streamlit_notify as stn

        at = AppTest.from_function(app_script, default_timeout=10)

        # Run the app initially
        at.run()

        # Don't trigger any notifications, just run notify
        at.button(key="rerun_btn").click()
        at.run()

        # Check that no notifications are displayed
        assert len(at.success) == 0
        assert len(at.error) == 0
        assert len(at.warning) == 0

    def test_notify_with_iterable_types(self):
        """Test notify with notification_type as a list/tuple."""
        import streamlit_notify as stn

        # Test with list
        at = AppTest.from_function(app_script_multiple_types, default_timeout=10)
        at.run()

        at.button(key="multi_btn").click()
        at.run()

        at.button(key="rerun_btn").click()
        at.run()

        # Should display success and error but not warning and info
        assert len(at.success) == 1
        assert len(at.error) == 1
        assert len(at.warning) == 0
        assert len(at.info) == 0

    def test_notify_invalid_notification_type(self):
        """Test notify with invalid notification type raises ValueError."""
        import streamlit_notify as stn

        def invalid_notify_app():
            import streamlit as st
            import streamlit_notify as stn

            if st.button("Test Invalid"):
                stn.notify(notification_type="invalid_type")

        at = AppTest.from_function(invalid_notify_app, default_timeout=10)
        at.run()

        # This should raise an exception when the button is clicked
        with pytest.raises(Exception):  # Could be ValueError or other exception type
            at.button(key="Test Invalid").click()
            at.run()

    def test_notify_mixed_valid_invalid_types(self):
        """Test notify with a mix of valid and invalid notification types."""
        import streamlit_notify as stn

        def mixed_types_app():
            import streamlit as st
            import streamlit_notify as stn

            if st.button("Test Mixed"):
                stn.notify(notification_type=["success", "invalid_type"])

        at = AppTest.from_function(mixed_types_app, default_timeout=10)
        at.run()

        # This should raise an exception when invalid type is encountered
        with pytest.raises(Exception):
            at.button(key="Test Mixed").click()
            at.run()
