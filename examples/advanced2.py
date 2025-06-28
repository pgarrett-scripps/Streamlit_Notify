import streamlit as st
import streamlit_notify as stn

# Loop over notifications and display those with valid data
for error_notification in stn.error.notifications.get_all():
    priority = error_notification.priority
    data = error_notification.data

    # Only show notifications with valid data (data=True)
    if data == True:
        error_notification.notify()
        stn.error.notifications.remove(error_notification)  # Remove the notification from the queue

st.write(f"Total Error Notifications: {len(stn.error.notifications)}")

# Will be shown
if st.button("Show Error Message1"):
    stn.error("Operation Error1!", data=True)
    st.rerun()

# Will not be shown
if st.button("Show Error Message2"):
    stn.error("Operation Error2!", data=False)
    st.rerun()
