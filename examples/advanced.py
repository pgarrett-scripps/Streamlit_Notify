import streamlit as st

import streamlit_notify as stn

c1, c2 = st.columns(2)

with c1:  # show only success messages in c1
    stn.success.notify()

with c2:  # show only error messages in c2
    stn.error.notify()

if st.button("Show Error Message"):
    stn.error("Operation failed!")
    st.rerun()

if st.button("Show Success Message"):
    stn.success("Operation successful!")
    st.rerun()
