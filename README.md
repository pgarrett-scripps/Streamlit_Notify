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

### Manual Control

```python
import streamlit as st
import streamlit_notify as stn

c1, c2 = st.columns(2)

with c1: # show only success messages in c1
    stn.success.notify()

with c2: # show only error messages in c2
    stn.error.notify()

if st.button("Show Error Message"):
    stn.error("Operation failed!")
    st.rerun()

if st.button("Show Success Message"):
    stn.success("Operation successful!")
    st.rerun()
```

### Advanced Control

```python
import streamlit as st
import streamlit_notify as stn

# loop over notifications and display those with valid data
for error_notification in stn.error.get_notifications():

    priority = error_notification.priority
    data = error_notification.data

    if data == True:
        error_notification.notify()

# will be shown
if st.button("Show Error Message1"):
    stn.error("Operation Error1!", data=True)
    st.rerun()

# will not be shown
if st.button("Show Error Message2"):
    stn.error("Operation Error2!", data=False)
    st.rerun()
```

## StatusElementNotification Class

The `StatusElementNotification` class is the core data structure that represents a notification within the system:

#### Attributes:

- `base_widget` (Callable): The original Streamlit widget function (e.g., st.success, st.error)
- `args` (OrderedDict[str, Any]): Arguments to pass to the base widget when displayed
- `priority` (int, optional): Priority of the notification, higher values displayed first (default: 0)
- `data` (Any, optional): Custom data that can be attached to the notification (default: None)

#### Methods:

- `notify()`: Displays the notification by calling the base widget with stored arguments
- `name` (property): Returns the name of the base widget function

#### Example:

```python
import streamlit as st
import streamlit_notify as stn

# Create custom StatusElementNotification
notification = stn.StatusElementNotification(
    base_widget=st.success,
    args={'body': 'My Message', 'icon': None},
    priority=1,
    data=None,
)
st.write(f"Displaying {notification.name} notification:")
notification.notify()

# Or create StatusElementNotification from a widget
notification = stn.error.create_notification(body='My Message', icon=None, priority=1, data=None)
st.write(f"Displaying {notification.name} notification:")
notification.notify()
```

## RerunnableStatusElement Class

The `RerunnableStatusElement` class is a wrapper class that adds notification queueing functionality to standard Streamlit widgets. It inherits from `NotificationQueue`, extending it with widget-specific functionality:

#### Attributes:

- `base_widget` (Callable): The original Streamlit widget function being wrapped
- `queue_name` (str): Name of the queue (used as key in session state)
- `queue` (StreamlitNotificationQueue): Underlying queue implementation

#### Methods:

- `__call__(*args, **kwargs)`: Creates and queues a notification when the widget is called
- `create_notification(*args, **kwargs)`: Creates a StatusElementNotification without adding it to the queue
- `notify(remove=True)`: Displays all queued notifications, optionally removing them from the queue
- `has_notifications()`: Checks if there are any notifications in the queue
- `clear_notifications()`: Clears all notifications from the queue
- `pop_notification()`: Removes and returns the highest priority notification
- `get_notifications()`: Gets all notifications in the queue
- `add_notification(notification)`: Adds a notification to the queue

## Custom Notification Queues

The `NotificationQueue` class allows you to create custom notification queues for specialized use cases:

```python
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
```
