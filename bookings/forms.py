from django import forms

class BookingDetailsForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "Your name"})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
    phone = forms.CharField(
        max_length=20,
        label="Phone Number (optional)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "07... or +44..."})
    )
    notes = forms.CharField(
        label="Additional Notes (optional)",
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Any extra info you'd like to share...",
            "rows": 4,
            "cols": 40
        })
    )
