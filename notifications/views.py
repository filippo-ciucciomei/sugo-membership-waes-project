from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Notification



# Create your views here.


@login_required
def mark_notifications_read(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return JsonResponse({"success": True})



@login_required
def notifications_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    )

    return render(
        request,
        "notifications/notifications_list.html",
        {"notifications": notifications}
    )