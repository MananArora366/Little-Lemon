from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Menu, Booking
from .serializers import MenuSerializer


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
        now = timezone.now()
        booking = Booking.objects.create(name="John Doe", no_of_guests=4, booking_date=now)
        self.assertEqual(booking.name, "John Doe")
        self.assertEqual(booking.no_of_guests, 4)

class WebViewTest(TestCase):
    def test_menu_page_renders(self):
        Menu.objects.create(title="Bruschetta", price=12.99, inventory=25)
        r = self.client.get(reverse('restaurant:web-menu'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Bruschetta")

    def test_booking_post_redirects(self):
        r = self.client.post(reverse('restaurant:web-book'), {
            "name": "Manan", 
            "no_of_guests": 4,
            "booking_date": "2026-08-20T19:00",
        })
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

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
