import streamlit as st
import streamlit_notify as stn

st.set_page_config(
    page_title="Streamlit-Notify Demo",
    page_icon="🔔",
    layout="centered"
)

with st.container(border=True):
    st.caption("Notifications will be shown here")
    # Display all queued notifications at the beginning
    stn.notify()

# Application title and description
st.title("🔔 Streamlit-Notify Demo")
st.markdown("""
This demo showcases the capabilities of the `streamlit-notify` package, 
which provides status elements that persist across reruns.
""")


st.header("Basic Notification Types")
st.markdown("Click any button to trigger a notification and rerun the app. ")

# Create a nice layout with columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Standard Elements")
    if st.button("Show Success", key="success_btn"):
        stn.success("Operation completed successfully!")
        st.rerun()
    
    if st.button("Show Info", key="info_btn"):
        stn.info("Here's some useful information.")
        st.rerun()
    
    if st.button("Show Warning", key="warning_btn"):
        stn.warning("This action might cause issues.")
        st.rerun()

with col2:
    st.subheader("Error & Exception")
    if st.button("Show Error", key="error_btn"):
        stn.error("An error occurred during the operation.")
        st.rerun()
    
    if st.button("Show Exception", key="exception_btn"):
        stn.exception("ValueError: This is a simulated exception")
        st.rerun()

with col3:
    st.subheader("Special Effects")
    if st.button("Show Toast", key="toast_btn"):
        stn.toast("This is a toast notification", icon="✅")
        st.rerun()
    
    if st.button("Show Balloons", key="balloons_btn"):
        stn.balloons()
        st.rerun()
    
    if st.button("Show Snow", key="snow_btn"):
        stn.snow()
        st.rerun()

st.markdown("---")
st.markdown("""
### Learn More
Check out the [documentation](https://streamlit-notify.readthedocs.io/) for more examples and API details.
""")

