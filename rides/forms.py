from django import forms
from .models import Ride
from .models import Comment



class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [
            "title",
            "description",
            "date",
            "time",
            "max_riders",
            "discipline",
            "gpx_file",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
        }

# Form for creating comments - only content field is needed, user and ride will be set in the view
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }