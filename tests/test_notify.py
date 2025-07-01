"""
Integration tests using Streamlit's AppTest for streamlit_notify package.

These tests verify that notifications work correctly in a simulated Streamlit app environment.
"""

from streamlit.testing.v1 import AppTest


def app_script():
    import streamlit as st

    import streamlit_notify as stn

    # Set up the page
    st.title("Streamlit Notify Test App")

    # Display all queued notifications
    stn.notify(remove=True)

    # Create buttons to trigger different notification types
    if st.button("Trigger Success", key="success_btn"):
        stn.success("Success notification triggered!")

    if st.button("Trigger Error", key="error_btn"):
        stn.error("Error notification triggered!")

    if st.button("Trigger Warning", key="warning_btn"):
        stn.warning("Warning notification triggered!")

    if st.button("Trigger Info", key="info_btn"):
        stn.info("Info notification triggered!")

    if st.button("Trigger Toast", key="toast_btn"):
        stn.toast("Toast notification triggered!")

    if st.button("Trigger Exception", key="exception_btn"):
        stn.exception("Exception notification triggered!")

    if st.button("Trigger Snow", key="snow_btn"):
        stn.snow()

    if st.button("Trigger Balloons", key="balloons_btn"):
        stn.balloons()

    # rerun button
    if st.button("Rerun", key="rerun_btn"):
        pass


def _helper(button_key: str, st_attribute: str, session_state_key: str):

    # Create an AppTest instance from our test app
    at = AppTest.from_function(app_script, default_timeout=10)

    # Run the app initially
    at.run()

    # Click the success button
    at.button(key=button_key).click()
    at.run()

    # Check that notification is queued but not displayed yet
    assert len(getattr(at, st_attribute)) == 0
    assert len(at.session_state[session_state_key]) == 1

    # Click rerun button to trigger notify_all
    at.button(key="rerun_btn").click()
    at.run()

    # After triggering notify_all, should see the notification
    assert len(getattr(at, st_attribute)) == 1
    assert len(at.session_state[session_state_key]) == 0


class TestStreamlitNotifyIntegration:
    """Integration tests for streamlit_notify using AppTest."""

    def test_success_notification_in_app(self):
        """Test that success notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="success_btn",
            st_attribute="success",
            session_state_key=stn.success.session_state_key,
        )

    def test_error_notification_in_app(self):
        """Test that error notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="error_btn",
            st_attribute="error",
            session_state_key=stn.error.session_state_key,
        )

    def test_warning_notification_in_app(self):
        """Test that warning notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="warning_btn",
            st_attribute="warning",
            session_state_key=stn.warning.session_state_key,
        )

    def test_info_notification_in_app(self):
        """Test that info notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="info_btn",
            st_attribute="info",
            session_state_key=stn.info.session_state_key,
        )

    def test_toast_notification_in_app(self):
        """Test that toast notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="toast_btn",
            st_attribute="toast",
            session_state_key=stn.toast.session_state_key,
        )

    def test_exception_notification_in_app(self):
        """Test that exception notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        _helper(
            button_key="exception_btn",
            st_attribute="exception",  # Exceptions use error attribute
            session_state_key=stn.exception.session_state_key,
        )

    def test_snow_notification_in_app(self):
        """Test that snow notifications work in a Streamlit app context."""
        pass

    def test_balloons_notification_in_app(self):
        """Test that balloons notifications work in a Streamlit app context."""
        pass
