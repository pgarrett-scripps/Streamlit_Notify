import streamlit as st

import streamlit_notify as stn

# Display all queued notifications at the beginning of your app. This will also clear the list.
stn.notify(remove=True)  # default behavior

# Add a notification that will be displayed on the next rerun
if st.button("Show Toast"):
    stn.toast("This is a toast message", icon="✅")
    st.rerun()

if st.button("Show Balloons"):
    stn.balloons()
    st.rerun()

if st.button("Show Success Message"):
    stn.success("Operation successful!")
    st.rerun()
