import streamlit as st
import streamlit_notify as stn
from streamlit_notify.functional import toast_stn

notification = stn.create_notification(
    "This is a test notification",
    priority=1,
    data={"key": "value"},
    notification_type="toast"
)

toast_notification_queue = stn.get_notification_queue("toast")

st.write(toast_notification_queue.get_all())

toast_notification_queue.append(notification)

toast_notifications = stn.get_notifications("toast")

st.write(toast_notifications)


if st.button("Show Notifications"):
    toast_stn("Toast (Default)")
    toast_stn("Toast (1)", priority=1, data={"key": "value"})


if st.button('notify'):
    stn.notify()
