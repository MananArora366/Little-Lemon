from django import forms
from .models import Booking

# This class automatically creates a secure HTML form based on the Booking model (Module 5)
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # '__all__' automatically includes all fields from the Booking model in the form
        fields = '__all__' 
        # We use 'widgets' to inject CSS classes into the generated HTML inputs for styling
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'no_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
