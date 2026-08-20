from django import forms
from django.utils import timezone
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

    def clean_no_of_guests(self):
        """Form-level validation for guest count (1 to 20)."""
        guests = self.cleaned_data.get('no_of_guests')
        if guests is None:
            raise forms.ValidationError("Please specify the number of guests.")
        if guests < 1:
            raise forms.ValidationError("You must book for at least 1 guest.")
        if guests > 20:
            raise forms.ValidationError("For parties larger than 20, please contact the restaurant directly.")
        return guests

    def clean_booking_date(self):
        """Form-level validation to prevent bookings in the past."""
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < timezone.now():
            raise forms.ValidationError("Booking date cannot be in the past. Please select an upcoming date and time.")
        return booking_date
