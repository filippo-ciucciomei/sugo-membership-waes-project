from .models import Notification

# Adds unread notification count and latest notifications to every template context
def unread_notifications_count(request):
    if request.user.is_authenticated:
        # Get all notifications for the user, newest first
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by("-created_at")
        # Count how many are unread
        unread_count = notifications.filter(is_read=False).count()
        # Get the 5 most recent notifications
        latest_notifications = notifications[:5]
    else:
        unread_count = 0
        latest_notifications = []
    return {
        "unread_notifications_count": unread_count,
        "latest_notifications": latest_notifications,
    }