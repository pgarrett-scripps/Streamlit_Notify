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

    if st.button("Trigger Success", key="success_btn"):
        stn.success("2", priority=2)
        stn.success("1", priority=1)
        stn.success("3", priority=3)

    # rerun button
    if st.button("Rerun", key="rerun_btn"):
        pass


class TestStreamlitNotifyIntegration:
    """Integration tests for streamlit_notify using AppTest."""

    def test_success_notification_in_app(self):
        """Test that success notifications work in a Streamlit app context."""
        import streamlit_notify as stn

        # Create an AppTest instance from our test app
        at = AppTest.from_function(app_script, default_timeout=10)

        # Run the app initially
        at.run()

        # Click the success button
        at.button(key="success_btn").click()
        at.run()

        # Check that notification is queued but not displayed yet
        assert len(getattr(at, "success")) == 0
        assert len(at.session_state[stn.success.session_state_key]) == 3

        # Click rerun button to trigger notify_all
        at.button(key="rerun_btn").click()
        at.run()

        # After triggering notify_all, should see the notification
        assert len(getattr(at, "success")) == 3
        assert len(at.session_state[stn.success.session_state_key]) == 0

        for i in range(3):
            assert getattr(at, "success")[i].body == str(3 - i)
