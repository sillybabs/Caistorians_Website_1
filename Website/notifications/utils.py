# notifications/utils.py
from .models import Notification, UserNotification

def create_notification(title, message, link=None, school=None, users=None):
    """
    Create a notification.
    - school: assign to a school (all users in school see it)
    - users: list of User objects for individual notifications
    """
    note = Notification.objects.create(title=title, message=message, link=link, school=school)
    
    if users:
        for user in users:
            UserNotification.objects.create(user=user, notification=note)
    return note


    """
    USAGE:
# School-wide notification
from notifications.utils import create_notification
create_notification(title="New Event", message="Check out the upcoming reunion!", school=school_obj)

# Individual notification
create_notification(title="New Message", message="You got a new message from Alice", users=[recipient_user], link="/messages/123/")


    """
