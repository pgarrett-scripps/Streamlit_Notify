Usage
=====

Rather than show notifications immediately, you can queue them up and display them at the beginning of your app. 
This is useful if you want to rerun your app and notify users of a change after the rerun.

Supported Status Elements
-------------------------

.. code-block:: python

    import streamlit_notify as stn

    # Use stn status widgets exactly like you would use a streamlit status widget
    stn.toast("This is a toast message", icon="✅")
    stn.balloons()
    stn.snow()
    stn.success("Operation successful!")
    stn.info("This is an info message")
    stn.error("This is an error message")
    stn.warning("This is a warning message")
    stn.exception("This is an exception message")


Basic Usage
-----------

By default, displaying a notification will also clear it from its associated queue, but you can change this behavior by 
specifying `remove=False` to any notify function.

.. code-block:: python

    import streamlit as st
    import streamlit_notify as stn

    # Display all queued notifications at the beginning of your app. This will also clear the list.
    stn.notify_all(remove=True) # default behavior

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


Other features
--------------

All stn status elements can be called exactly like their Streamlit counterpart, but come with some additional 
features. For example, stn.success is actually a `RerunnableStatusElement` with the following methods:

.. code-block:: python

    import streamlit_notify as stn

    # Queue a success message
    stn.success("Operation successful!")  # Adds a success notification to the queue

    # Create the underlying notification object without adding it to the queue
    success_notification = stn.success.create_notification("Operation successful!")
    print(success_notification)

    # Display all success notifications but don't delete them from the queue
    stn.success.notify(remove=False)
    stn.success.notify()  # Same but removes the notifications from the queue

    # Check if there are any notifications in the success queue
    has_notification = len(stn.success.notifications) > 0

    # Clear the success notification queue
    stn.success.notifications.clear()

    # Get the first notification from the success queue
    popped_notification = stn.success.notifications.pop()

    # Add a notification to the success queue
    stn.success.notifications.append(success_notification)

    # Get all notifications in the success queue  
    notifications = stn.success.notifications.get_all()

    # You can also display the notification directly
    success_notification.notify()  # Displays the notification


Notification Priority
---------------------

You can set priorities for notifications, with higher priority notifications displayed first. 
Otherwise, notifications are displayed in the order they were added:

.. code-block:: python

    # Higher priority notifications are displayed first
    stn.info("High priority message", priority=10)
    stn.info("Low priority message", priority=-5)

Adding Custom Data to Notifications
-----------------------------------

You can attach custom data to notifications:

.. code-block:: python

    # Attach data to notifications
    stn.info("Message with string data", data="Hello World")
    stn.info("Message with dictionary data", data={'Hello': 'World'})

Accessing Notifications
-----------------------

You can access notifications in different ways:

.. code-block:: python

    # Get notifications by type
    notifications = stn.get_all_notifications()
    error_notifications = notifications['error']
    toast_notifications = notifications['toast']

    # Or get them directly from the widget
    error_notifications = stn.error.notifications.get_all()

Managing Notifications
----------------------

Clear notifications when you no longer need them:

.. code-block:: python

    # Clear all notifications
    stn.clear_all_notifications()

    # Clear notifications of only a specific type
    stn.error.notifications.clear()

    # Check if any notifications exist
    has_notifications = stn.has_any_notifications()
    
    # Check for specific type
    has_errors = len(stn.error.notifications) > 0


Advanced Usage
--------------

For more advanced control, you can:

.. code-block:: python

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


Super Advanced Usage
--------------------

.. code-block:: python

    import streamlit as st
    import streamlit_notify as stn

    # Loop over notifications and display those with valid data
    for error_notification in stn.error.notifications.get_all():
        priority = error_notification.priority
        data = error_notification.data

        # Only show notifications with valid data (data=True)
        if data == True:
            error_notification.notify()

    # Will be shown
    if st.button("Show Error Message1"):
        stn.error("Operation Error1!", data=True)
        st.rerun()

    # Will not be shown
    if st.button("Show Error Message2"):
        stn.error("Operation Error2!", data=False)
        st.rerun()


Where are Status Elements Stored?
---------------------------------

The status elements are stored in a session state queue, under the key: `ST_NOTIFY_{WIDGETNAME}_QUEUE`.

For example, stn.success would be stored by the key: `ST_NOTIFY_SUCCESS_QUEUE`


What are Status Elements?
-------------------------

Status elements are special notifications that are displayed in the Streamlit app, such as toasts, 
balloons, and success messages. They can be used to provide feedback to users about the status of their 
actions or the state of the application.

They are stored as a dataclass `StatusElementNotification`, please refer to the :doc:`dclass documentation <api/dclass>` 
for more details.

For more examples, please refer to the :doc:`API documentation <api/index>`.
They are stored as a dataclass `StatusElementNotification`, please refer to the :doc:`dclass documentation <api/dclass>` 
for more details.

For more examples, please refer to the :doc:`API documentation <api/index>`.
