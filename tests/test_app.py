"""
Simple test app for streamlit_notify integration testing.
"""

import streamlit as st
import streamlit_notify as stn

# Set up the page
st.title("Streamlit Notify Test App")

# Display all queued notifications
stn.notify_all(remove=True)

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
