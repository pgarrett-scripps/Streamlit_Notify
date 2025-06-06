# Streamlit-Notify

A Streamlit component that provides status elements that persist across reruns.

Demo App: https://st-notify.streamlit.app/

![Demo](gif/demo.gif)


## Installation

```bash
pip install streamlit-notify
```

## Documentation

Full documentation is available at [Read the Docs](https://streamlit-notify.readthedocs.io/).

To build the documentation locally:

```bash
cd docs
pip install -r requirements.txt
make html
```

Then open `docs/build/html/index.html` in your browser.

## Supported Status Elements

- `stn.toast`: Toast notifications
- `stn.balloons`: Balloon animations
- `stn.snow`: Snow animations
- `stn.success`: Success messages
- `stn.info`: Info messages
- `stn.error`: Error messages
- `stn.warning`: Warning messages
- `stn.exception`: Exception messages

## How It Works

This package wraps standard Streamlit status element to enable queueing. Notifications are stored in Streamlit's session state and displayed during the next rerun cycle.

## Basic Usage

```python
import streamlit as st
import streamlit_notify as stn

# Display all queued notifications at the beginning of your app. This will also clear the list.
stn.notify_all()

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
```

#### Priority Support

```python
# Higher priority notifications are displayed first
stn.info("High priority message", priority=10)
stn.info("Low priority message", priority=-5)
```

#### Passing User Data

```python
# Higher priority notifications are displayed first
stn.info("High priority message", data="Hello World")
stn.info("Low priority message", data={'Hello': 'World'})
```

#### Getting all notifications

```python
# returns a dict mapping notification types to list of notifications
notifications = stn.get_all_notifications()
error_notifications = notifications['error']
toast_notifications = notifications['toast']

# or you can get the notifications directly from the stn widget
error_notifications = stn.error.get_notifications()
```

#### Clearing notifications

```python
# clears all notifications
stn.clear_all_notifications()

# clears notifications of only a specific type
stn.error.clear_notifications()
```

#### Checking if any notifications need to be shown

```python
# check if any notifications exist across all types
stn.has_any_notifications()

# check only specific type
stn.error.has_notifications()
```