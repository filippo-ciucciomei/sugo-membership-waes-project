from django.urls import path
from .views import membership_required, create_checkout_session, stripe_webhook, membership_success, membership_cancel

urlpatterns = [
    path("", membership_required, name="membership_required"),
    path("checkout/", create_checkout_session, name="membership_checkout"),
    path("success/", membership_success, name="membership_success"),
    path("cancel/", membership_cancel, name="membership_cancel"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
]