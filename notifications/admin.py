
from django.contrib import admin
from .models import Notification

# Register your models here.

# Admin panel settings for Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("recipient", "actor", "ride", "type", "is_read", "created_at")
    # Add filters for type, read status, date, and recipient
    list_filter = ("type", "is_read", "created_at", "recipient")




# @admin.register(MembershipPlan)
# class MembershipPlanAdmin(admin.ModelAdmin):
#     list_display = ("name", "price", "duration_days", "is_active")
#     list_filter = ("is_active",)
    
# @admin.register(MembershipPurchase)
# class MembershipPurchaseAdmin(admin.ModelAdmin):
#     list_display = ("user", "plan", "start_date", "expiry_date", "price_paid", "is_active")
#     list_filter = ("plan", "start_date", "expiry_date", "user")