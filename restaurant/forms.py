from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # Explicit fields declaration prevents accidental exposure of internal model fields
        fields = ['name', 'no_of_guests', 'booking_date']
        
        # HTML form styling and input attributes
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'no_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '20'}),
        }

    # NOTE: guest-count and past-date rules are NOT repeated here on purpose.
    # They live as validators on the Booking model (models.py), so they apply
    # everywhere at once: this form, the DRF API, the admin, and shell writes.
    # ModelForm runs those model validators automatically during full_clean(),
    # so duplicating them as clean_<field>() methods only creates two competing
    # error messages for the same rule.
