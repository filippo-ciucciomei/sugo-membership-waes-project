from django.contrib import admin
from .models import MembershipPlan, MembershipPurchase


# Register your models here.

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "duration_days", "is_active")
    list_filter = ("is_active",)
    
@admin.register(MembershipPurchase)
class MembershipPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "expiry_date", "price_paid", "is_active")
    list_filter = ("plan", "start_date", "expiry_date", "user")