
from django import forms

from officer.models import CitizenRequest


class CitizenRequestForm(forms.ModelForm):
    class Meta:
        model = CitizenRequest
        fields = [
            "subject",
            "description",
            "department",
            "service",
            "district",
        ]
        widgets = {
            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "What service or action are you requesting?",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Describe your request...",
            }),
            "department": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Responsible government department",
            }),
            "service": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Service requested (optional)",
            }),
            "district": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "District where assistance is needed",
            }),
        }
