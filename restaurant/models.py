from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.SmallIntegerField()

    def get_item(self):
        return f"{self.title} : {str(self.price)}"

    def __str__(self):
        return f"{self.title} : {str(self.price)}"


class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Number of guests must be at least 1."),
            MaxValueValidator(20, message="Maximum booking capacity is 20 guests per table.")
        ]
    )
    booking_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} for {self.no_of_guests} guests on {self.booking_date.strftime('%Y-%m-%d %H:%M')}"
