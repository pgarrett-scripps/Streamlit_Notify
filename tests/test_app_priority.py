"""
Simple test app for streamlit_notify integration testing.
"""

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
