from django.contrib import admin
from .models import MembershipPlan, MembershipPurchase

# Register your models here.

# Admin panel settings for MembershipPlan
@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("name", "price", "duration_days", "is_active")
    # Add a filter for active/inactive plans
    list_filter = ("is_active",)

# Admin panel settings for MembershipPurchase
@admin.register(MembershipPurchase)
class MembershipPurchaseAdmin(admin.ModelAdmin):
    # Show these fields in the list view
    list_display = ("user", "plan", "start_date", "expiry_date", "price_paid", "is_active")
    # Add filters for plan, dates, and user
    list_filter = ("plan", "start_date", "expiry_date", "user")