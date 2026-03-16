from django.test import TestCase
from .forms import CommentForm
from .forms import RideForm

class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        form = CommentForm({'content': 'Great ride!'})
        self.assertTrue(form.is_valid(), msg="Form is not valid")


    def test_form_is_invalid(self):
        form = CommentForm({'content': ''})
        self.assertFalse(form.is_valid(), msg="Form is valid")


class TestRideForm(TestCase):

    def test_form_is_valid(self):
        form = RideForm({
            'title': 'Morning Ride',
            'description': 'Fast laps in Regents Park',
            'date': '2026-04-10',
            'time': '07:00',
            'max_riders': 10,
            'discipline': 'road',
        })
        self.assertTrue(form.is_valid(), msg="RideForm should be valid")

    def test_form_invalid_without_title(self):
        form = RideForm({
            'title': '',
            'description': 'Fast laps in Regents Park',
            'date': '2026-04-10',
            'time': '07:00',
            'max_riders': 10,
            'discipline': 'road',
        })
        self.assertFalse(form.is_valid(), msg="RideForm is valid without title")

    def test_form_invalid_without_date(self):
        form = RideForm({
            'title': 'Morning Ride',
            'description': 'Fast laps in Regents Park',
            'date': '',
            'time': '07:00',
            'max_riders': 10,
            'discipline': 'road',
        })
        self.assertFalse(form.is_valid(), msg="RideForm is valid without date")

    def test_form_invalid_without_time(self):
        form = RideForm({
            'title': 'Morning Ride',
            'description': 'Fast laps in Regents Park',
            'date': '2026-04-10',
            'time': '',
            'max_riders': 10,
            'discipline': 'road',
        })
        self.assertFalse(form.is_valid(), msg="RideForm is valid without time")