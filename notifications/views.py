from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Notification



# Create your views here.


@login_required
    # Mark all notifications as read for the current user
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)
    return JsonResponse({"success": True})



@login_required
    # Show a list of notifications for the current user
    notifications = Notification.objects.filter(
        recipient=request.user
    )
    return render(
        request,
        "notifications/notifications_list.html",
        {"notifications": notifications}
    )