from django.utils import timezone
from membership.models import MembershipPurchase

# Adds membership status and expiry info to every template context
def membership_status_and_expiry(request):
    user = request.user
    status = None
    expiry = None
    if user.is_authenticated:
        # Find the user's most recent active membership
        purchase = (
            MembershipPurchase.objects.filter(user=user, expiry_date__gte=timezone.now().date())
            .order_by('-expiry_date')
            .first()
        )
        if purchase:
            status = 'Active'
            expiry = purchase.expiry_date
        else:
            # If no active membership, check for any previous membership
            last_purchase = (
                MembershipPurchase.objects.filter(user=user)
                .order_by('-expiry_date')
                .first()
            )
            if last_purchase:
                status = 'Expired'
                expiry = last_purchase.expiry_date
            else:
                status = 'None'
                expiry = None
    return {
        'user_membership_status': status,
        'user_membership_expiry': expiry,
    }
