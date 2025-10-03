from django import forms
from .models import CheckoutFeedback

class CheckoutFeedbackForm(forms.ModelForm):
    anonymous = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Post without showing a name"
    )

    class Meta:
        model = CheckoutFeedback
        fields = ["name", "message", "anonymous"]
        labels = {"message": "Short statement"}
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your name (optional)"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "How was the checkout process?"
            }),
        }
