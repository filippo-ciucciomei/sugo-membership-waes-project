from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import date

from .models import Ride
from .forms import CommentForm

from membership.models import MembershipPlan, MembershipPurchase


class TestRideViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.plan = MembershipPlan.objects.create(
            name="Annual Membership",
            price=3000,
            duration_days=365,
            is_active=True
        )

        self.purchase = MembershipPurchase.objects.create(
            user=self.user,
            plan=self.plan
        )

        self.ride = Ride.objects.create(
            user=self.user,
            title="Morning Ride",
            description="Fast laps in Regents Park",
            date=date(2026, 4, 10),
            time="07:00",
            max_riders=10,
            discipline="road",
        )

    def test_render_ride_detail_page_with_comment_form(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("ride_detail", args=[self.ride.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Morning Ride", response.content)
        self.assertIn(b"Fast laps in Regents Park", response.content)
        self.assertIsInstance(response.context["comment_form"], CommentForm)

    
    def test_successful_comment_submission(self):
        self.client.login(username="testuser", password="testpass123")

        post_data = {
            "content": "This is a test comment."
        }

        response = self.client.post(
            reverse("ride_detail", args=[self.ride.slug]),
            post_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.ride.comments.count(), 1)
        self.assertEqual(
            self.ride.comments.first().content,
            "This is a test comment."
        )