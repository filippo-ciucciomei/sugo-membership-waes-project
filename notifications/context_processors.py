from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:

        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by("-created_at")

        unread_count = notifications.filter(is_read=False).count()

        latest_notifications = notifications[:5]

    else:
        unread_count = 0
        latest_notifications = []

    return {
        "unread_notifications_count": unread_count,
        "latest_notifications": latest_notifications,
    }