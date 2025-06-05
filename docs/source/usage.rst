Usage
=====

Rather than show notification immediatly, you can queue them up and display them at the beginning of your app. 
This is useful if you want to rerun your app and notify users of a change after the rerun.

Supported Status Elements
-----------

.. code-block:: python

    import streamlit_notify as stn

    # use stn status widgets exactly like you would use a streamlit status widget
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

By default,
displaying a notification will also clear it from it's asscoiated the queue, but you can change this behavior by 
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
---------------------

All stn status elements can be called exactly like their streamlit counterpart, but come with some additional 
features. For example, stn.success is actually a `RerunnableStatusElement` with the following methods:

.. code-block:: python

    import streamlit_notify as stn

    # queue a success message
    stn.success("Operation successful!")  # Displays a success message

    # create the underlying notification object without displaying it
    # Creates a notification without displaying it
    success_notification: stn.RerunnableStatusElement = stn.success.create_notification("Operation successful!")  
    print(success_notification)

    # Displays all success notification but doesnt delete them from the queue
    stn.success.notify(remove=False)
    stn.success.notify()  #  Same but removes the notification from the queue
    
    # Checks if there are any notifications in the success queue
    has_notification: bool = stn.success.has_notifications()  

    # Clear the success notification queue
    stn.success.clear_notifications()  

    # Get the first notification from the success queue
    popped_notification: stn.RerunnableStatusElement | None = stn.success.pop_notification()

    # Adds a notification to the success queue
    stn.success.add_notification(success_notification)

    # Gets all notifications in the success queue  
    notifications: list[stn.RerunnableStatusElement] = stn.success.get_notifications()  

    # can also display the notification directly
    success_notification.notify()  # Displays the notification and removes it from the queue


Notification Priority
---------------------

You can set priorities for notifications, with higher priority notifications displayed first. 
Otherwise, notifications are displayed in the order they were added:

.. code-block:: python

    # Higher priority notifications are displayed first
    stn.info("High priority message", priority=10)
    stn.info("Low priority message", priority=-5)

Adding Custom Data to Notifications
------------------------------

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
    error_notifications = stn.error.get_notifications()

Managing Notifications
----------------------

Clear notifications when you no longer need them:

.. code-block:: python

    # Clear all notifications
    stn.clear_all_notifications()

    # Clear notifications of only a specific type
    stn.error.clear_notifications()

    # Check if any notifications exist
    has_notifications = stn.has_any_notifications()
    
    # Check for specific type
    has_errors = stn.error.has_notifications()


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
--------------

.. code-block:: python

    import streamlit as st
    import streamlit_notify as stn

    # loop over notifications and display those with valid data
    for error_notification in stn.error.get_notifications():

        priority = error_notification.priority
        data = error_notification.data

        # only show notifications with valid data (data=True)
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



Where are Status Elements Stored?
-----------

The status elements are stored in a session state queue, under the key: `ST_NOTIFY_{WIDGETNAME}_QUEUE.`

For example, stn.success would be stored by the key: `ST_NOTIFY_SUCCESS_QUEUE`


What are Status Elements?
-----------

Status elements are special notifications that are displayed in the Streamlit app, such as toasts, 
balloons, and success messages. They can be used to provide feedback to users about the status of their 
actions or the state of the application.

They are stored a dataclass `StatusElementNotification`, please refer to the :doc:`dclass documentation <api/dclass>` 
for more details.

For more examples, please refer to the :doc:`API documentation <api/index>`.
