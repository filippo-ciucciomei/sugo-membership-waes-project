from django.urls import path
from .views import (
    membership_required,
    create_checkout_session,
    stripe_webhook,
    membership_success,
    membership_cancel,
    membership_checkout_page,
    PostLoginRedirectView,
)

urlpatterns = [
    path("", membership_required, name="membership_required"),
    path("checkout/stripe/", create_checkout_session, name="membership_checkout_stripe"),
    path("checkout/", membership_checkout_page, name="membership_checkout"),
    path("success/", membership_success, name="membership_success"),
    path("cancel/", membership_cancel, name="membership_cancel"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
    path("post-login/", PostLoginRedirectView.as_view(), name="post_login_redirect"),
]