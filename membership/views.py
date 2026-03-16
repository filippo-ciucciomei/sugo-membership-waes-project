
# membership/views.py

# Import necessary Django modules for handling HTTP requests, rendering templates, and managing user sessions
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Import models for membership plans and purchases
from .models import MembershipPlan, MembershipPurchase


# Import Stripe for payment processing
import stripe



# Set the Stripe API key from Django settings
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.


# Check if a user has an active membership (not expired)
def user_has_active_membership(user):
    if not user.is_authenticated:
        return False
    # Look for any membership purchases that have not expired
    return MembershipPurchase.objects.filter(
        user=user,
        expiry_date__gte=timezone.now().date()
    ).exists()


# Show a page explaining membership status and options
def membership_required(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    # Get all purchases for this user
    purchases = MembershipPurchase.objects.filter(user=request.user).order_by("-created_at")
    has_active = purchases.filter(expiry_date__gte=timezone.now().date()).exists()
    has_previous = purchases.exists()

    # Decide what message and button to show
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


# Create a Stripe checkout session for buying or renewing membership
@require_GET
def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    # Get the first active membership plan
    plan = MembershipPlan.objects.filter(is_active=True).first()

    if not plan:
        return JsonResponse({"error": "No active membership plan found."}, status=400)

    # Create a Stripe checkout session with plan details
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




# Show the success page after payment
def membership_success(request):
    return render(request, "membership/membership_success.html")

# Show the cancel page if payment is cancelled
def membership_cancel(request):
    return render(request, "membership/membership_cancel.html")

# Show the Stripe checkout page
def membership_checkout_page(request):
    if not request.user.is_authenticated:
        return redirect("account_login")

    return render(
        request,
        "membership/membership_checkout.html",
        {"STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY}
    )


# After login, send user to the right page based on membership status
class PostLoginRedirectView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")

        if user_has_active_membership(request.user):
            return redirect("home")

        return redirect("membership_required")


# Handle Stripe webhook events (like payment completed)
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        # Verify the event is from Stripe
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

        # If payment is completed, create a new membership purchase
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
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    except Exception:
        # Other errors
        return HttpResponse(status=500)