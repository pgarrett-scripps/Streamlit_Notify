import streamlit_notify as stn

# queue a success message
stn.success("Operation successful!")  # Displays a success message

# create the underlying notification object without displaying it
success_notification: stn.RerunnableStatusElement = stn.success.create_notification("Operation successful!")  # Creates a notification without displaying it
print(success_notification)

stn.success.notify()  # Displays all success notifications and them from the success queue
stn.success.notify(remove=False)  # Displays all success notification but doesnt delete them from the queue
has_notification: bool = stn.success.has_notifications()  # Checks if there are any notifications in the success queue
stn.success.clear_notifications()  # Clears the success notification queue
popped_notification: stn.RerunnableStatusElement | None = stn.success.pop_notification()  # Pops a notification from the success queue
stn.success.add_notification(success_notification)  # Adds a notification to the success queue
notifications: list[stn.RerunnableStatusElement] = stn.success.get_notifications()  # Gets all notifications in the success queue
