from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(item.get_item(), "IceCream : 80")
        self.assertEqual(str(item), "IceCream : 80")


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item1 = Menu.objects.create(title="Bruschetta", price=12.99, inventory=25)
        self.item2 = Menu.objects.create(title="Lemon Dessert", price=8.50, inventory=15)

    def test_getall(self):
        response = self.client.get(reverse('restaurant:menu-list'))
        items = Menu.objects.all()
        serializer = MenuSerializer(items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_item(self):
        payload = {"title": "Greek Salad", "price": "14.50", "inventory": 30}
        response = self.client.post(reverse('restaurant:menu-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)


class BookingModelTest(TestCase):
    def test_booking_creation(self):
        now = timezone.now() + timezone.timedelta(days=1)
        booking = Booking.objects.create(name="John Doe", no_of_guests=4, booking_date=now)
        self.assertEqual(booking.name, "John Doe")
        self.assertEqual(booking.no_of_guests, 4)

    def test_model_full_clean_rejects_past_date(self):
        past_date = timezone.now() - timezone.timedelta(days=1)
        booking = Booking(name="Time Traveler", no_of_guests=4, booking_date=past_date)
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_model_full_clean_rejects_invalid_guests(self):
        future_date = timezone.now() + timezone.timedelta(days=1)
        booking_negative = Booking(name="Bad Guest", no_of_guests=0, booking_date=future_date)
        with self.assertRaises(ValidationError):
            booking_negative.full_clean()

        booking_overflow = Booking(name="Party of 50", no_of_guests=50, booking_date=future_date)
        with self.assertRaises(ValidationError):
            booking_overflow.full_clean()


class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_rejects_past_date(self):
        past_date = (timezone.now() - timezone.timedelta(days=10)).isoformat()
        payload = {
            "name": "API Past Date",
            "no_of_guests": 4,
            "booking_date": past_date,
        }
        response = self.client.post('/restaurant/booking/tables/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("booking_date", response.data)

    def test_api_rejects_invalid_guests(self):
        future_date = (timezone.now() + timezone.timedelta(days=2)).isoformat()
        payload = {
            "name": "API Invalid Guests",
            "no_of_guests": -5,
            "booking_date": future_date,
        }
        response = self.client.post('/restaurant/booking/tables/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("no_of_guests", response.data)

    def test_api_accepts_valid_booking(self):
        future_date = (timezone.now() + timezone.timedelta(days=2)).isoformat()
        payload = {
            "name": "API Valid Guest",
            "no_of_guests": 4,
            "booking_date": future_date,
        }
        response = self.client.post('/restaurant/booking/tables/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)


class WebViewTest(TestCase):
    def test_menu_page_renders(self):
        Menu.objects.create(title="Bruschetta", price=12.99, inventory=25)
        r = self.client.get(reverse('restaurant:web-menu'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Bruschetta")

    def test_booking_post_redirects(self):
        future_date = (timezone.now() + timezone.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        r = self.client.post(reverse('restaurant:web-book'), {
            "name": "Manan", 
            "no_of_guests": 4,
            "booking_date": future_date,
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_negative_guests_rejected(self):
        future_date = (timezone.now() + timezone.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
        r = self.client.post(reverse('restaurant:web-book'), {
            "name": "Bad Guest",
            "no_of_guests": -5,
            "booking_date": future_date,
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_past_date_rejected(self):
        r = self.client.post(reverse('restaurant:web-book'), {
            "name": "Time Traveler",
            "no_of_guests": 4,
            "booking_date": "2020-01-01T10:00",
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)

    def test_single_menu_item_renders(self):
        item = Menu.objects.create(title="Tiramisu", price=9.99, inventory=10)
        r = self.client.get(reverse('restaurant:web-menu-item', kwargs={'pk': item.pk}))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Tiramisu")

    def test_single_menu_item_404_on_missing_id(self):
        r = self.client.get(reverse('restaurant:web-menu-item', kwargs={'pk': 999}))
        self.assertEqual(r.status_code, 404)

    def test_empty_menu_renders_empty_state(self):
        r = self.client.get(reverse('restaurant:web-menu'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "No items on the menu yet.")
