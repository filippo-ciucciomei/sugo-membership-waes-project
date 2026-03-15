from django import forms
from .models import Ride
from .models import Comment

# Form for creating and editing rides
class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        # Fields to show in the form
        fields = [
            "title",
            "description",
            "date",
            "time",
            "max_riders",
            "discipline",
            "gpx_file",
        ]
        # Use special widgets for date and time fields
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

# Form for creating comments - only content field is needed, user and ride will be set in the view
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        # Use a textarea for the comment content
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }