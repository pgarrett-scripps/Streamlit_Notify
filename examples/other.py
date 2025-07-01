import streamlit_notify as stn

# Queue a success message
stn.success("Operation successful!")  # Adds a success notification to the queue

# Create the underlying notification object without adding it to the queue
success_notification = stn.success.create_notification("Operation successful!")
print(success_notification)

# Display all success notifications but don't delete them from the queue
stn.success.notify(remove=False)
stn.success.notify()  # Same but removes the notifications from the queue

# displayed 2x

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

# 3x
