from django import forms
from .models import Ride


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