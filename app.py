from typing import Dict
import streamlit as st
import streamlit_notify as stn


# Create a custom notification queue
custom_queue = stn.NotificationQueue(queue_name='my_notification_queue')

# Display all notifications in the custom queue
custom_queue.notify()

if st.button("Add Custom Notification"):
    # Create a notification using StatusElementNotification
    success_notification = stn.StatusElementNotification(
        base_widget=st.success,
        args={'body': 'My Message', 'icon': None},
        priority=1,
        data=None,
    )
    custom_queue.add_notification(success_notification)
    
    # You can add multiple notifications to the same queue
    error_notification = stn.StatusElementNotification(
        base_widget=st.error,
        args={'body': 'Error Message', 'icon': None},
        priority=2,
        data=None,
    )
    custom_queue.add_notification(error_notification)
    st.rerun()


# returns a dict mapping notification types to list of notifications
notifications = stn.get_all_notifications()
error_notifications = notifications['error']
toast_notifications = notifications['toast']

# or you can get the notifications directly from the stn widget
error_notifications = stn.error.get_notifications()

for error_notification in error_notifications:

    priority = error_notification.priority
    data = error_notification.data

    if data == True:
        error_notification.notify()


if st.button("Show Error Message1"):
    stn.error("Operation Error1!", data=True)
    st.rerun()

if st.button("Show Error Message2"):
    stn.error("Operation Error2!", data=False)
    st.rerun()

stn.notify_all(True)

print(stn.toast.create_notification("This is a custom toast message", icon="ℹ️"))

if st.button("Add st toast"):
    st.toast("Info", icon="ℹ️")

if st.button("Add Success Toast"):
    stn.toast("Success2", icon="✅", priority=2)
    stn.toast("Success3", icon="✅", priority=3)
    stn.toast("Success1", icon="✅", priority=1)
    st.rerun()
    
if st.button("Add Error Toast"):
    stn.toast("Error", icon="✅")
    st.rerun()
    
if st.button("Add Material Icon Toast"):
    stn.toast("Material", icon="✅")
    st.rerun()

if st.button("Rerun"):
    st.rerun()

if st.button("Balloons"):
    stn.balloons()
    st.rerun()

if st.button("Snow"):
    stn.snow()
    st.rerun()

if st.button("Success"):
    stn.success("Success")
    st.rerun()

if st.button("Info"):
    stn.info("Info")
    st.rerun()

if st.button("Error"):
    stn.error("Error1", priority=1)
    stn.error("Error3", priority=1)
    stn.error("Error2", priority=1)

    st.rerun()

if st.button("Warning"):
    stn.warning("Warning")
    st.rerun()

if st.button("Exception"):
    stn.exception("Exception")
    st.rerun()