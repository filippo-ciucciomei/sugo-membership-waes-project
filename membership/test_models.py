from django.test import TestCase
from django.contrib.auth.models import User
from membership.models import MembershipPlan, MembershipPurchase


class TestMembershipModels(TestCase):

    def test_membership_expiry_date_is_set(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        plan = MembershipPlan.objects.create(
            name="Annual Membership",
            price=3000,
            duration_days=365,
            is_active=True
        )

        purchase = MembershipPurchase.objects.create(
            user=user,
            plan=plan
        )

        self.assertIsNotNone(purchase.expiry_date)
        self.assertTrue(purchase.is_active)