from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import MembershipPlan, MembershipPurchase

import stripe


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
@require_GET
def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    plan = MembershipPlan.objects.filter(is_active=True).first()

    if not plan:
        return JsonResponse({"error": "No active membership plan found."}, status=400)

    session = stripe.checkout.Session.create(
        ui_mode="embedded",
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
        return_url=request.build_absolute_uri("/membership/success/") + "?session_id={CHECKOUT_SESSION_ID}",
        metadata={
            "user_id": request.user.id,
            "plan_id": plan.id,
            "type": "renewal",
        },
    )

    return JsonResponse({"clientSecret": session.client_secret})



# redirect to the success page after successful checkout
def membership_success(request):
    return render(request, "membership/membership_success.html")

def membership_cancel(request):
    return render(request, "membership/membership_cancel.html")

def membership_checkout_page(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    return render(
        request,
        "membership/membership_checkout.html",
        {"STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY}
    )

# View to handle post-login redirection based on the user's membership status. 
# If the user has an active membership, they are redirected to the home page; 
# otherwise, they are redirected to the membership required page.
class PostLoginRedirectView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        if user_has_active_membership(request.user):
            return redirect("home")

        return redirect("membership_required")
    

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

    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    except Exception:
        return HttpResponse(status=500)