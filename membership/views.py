from django.shortcuts import render, redirect
from django.utils import timezone
from .models import MembershipPlan, MembershipPurchase

import stripe
from django.conf import settings

from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

#Create your views here.

# Helper function to check if a user has an active membership by querying the MembershipPurchase model for any records with an expiry date in the future.
def user_has_active_membership(user):
    if not user.is_authenticated:
        return False

    return MembershipPurchase.objects.filter(
        user=user,
        expiry_date__gte=timezone.now().date()
    ).exists()

# View to check if the user has an active membership and display appropriate messages and options for purchasing or renewing a membership plan.
def membership_required(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    purchases = MembershipPurchase.objects.filter(user=request.user).order_by("-created_at")
    has_active = purchases.filter(expiry_date__gte=timezone.now().date()).exists()
    has_previous = purchases.exists()

    if has_active:
        button_text = None
        message = "Your membership is already active."
    elif has_previous:
        button_text = "Renew Membership"
        message = "Your membership has expired. Renew it to access rides."
    else:
        button_text = "Buy Membership"
        message = "You need a membership to access rides."

    context = {
        "has_active_membership": has_active,
        "has_previous_membership": has_previous,
        "button_text": button_text,
        "message": message,
    }

    return render(request, "membership/membership_required.html", context)

# View to create a Stripe checkout session for purchasing or renewing a membership plan. 
# It checks if the user is authenticated and if there is an active membership plan available, 
# then creates a checkout session with the plan details and redirects the user to the Stripe checkout page.
def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    plan = MembershipPlan.objects.filter(is_active=True).first()

    if not plan:
        return redirect("membership_required")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": plan.name,
                    },
                    "unit_amount": plan.price,
                },
                "quantity": 1,
            }
        ],
        success_url=request.build_absolute_uri("/membership/success/"),
        cancel_url=request.build_absolute_uri("/membership/cancel/"),
        metadata={
            "user_id": request.user.id,
            "plan_id": plan.id,
            "type": "renewal",
        },
    )

    return redirect(session.url, code=303)


from django.http import HttpResponse
import json

# Stripe webhook to handle checkout session completion and create a MembershipPurchase record for the user.
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        user_id = session["metadata"]["user_id"]
        plan_id = session["metadata"]["plan_id"]

        from django.contrib.auth import get_user_model
        User = get_user_model()

        user = User.objects.get(id=user_id)
        plan = MembershipPlan.objects.get(id=plan_id)

        MembershipPurchase.objects.create(
            user=user,
            plan=plan,
            price_paid=plan.price
        )

    return HttpResponse(status=200)


# redirect to the success page after successful checkout
def membership_success(request):
    return render(request, "membership/membership_success.html")

def membership_cancel(request):
    return render(request, "membership/membership_cancel.html")