from streamlit_notify.extras import toast_stn, create_notification, notify, get_notifications, get_notification_queue
import streamlit as st

notification = create_notification(
    "This is a test notification",
    priority=1,
    data={"key": "value"},
    notification_type="toast"
)

toast_notification_queue = get_notification_queue("toast")

st.write(toast_notification_queue.get_all())

toast_notification_queue.append(notification)

toast_notifications = get_notifications("toast")

st.write(toast_notifications)


if st.button("Show Notifications"):
    toast_stn("Toast (Default)")
    toast_stn("Toast (1)", priority=1, data={"key": "value"})


if st.button('notify'):
    notify()
