from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


def index(request):
    """Render the Little Lemon home/landing page."""
    return render(request, 'index.html', {})


class MenuItemsView(generics.ListCreateAPIView):
    """API view to list all menu items or create a new menu item."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """API view to get, update, or delete a single menu item by ID."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    """ModelViewSet to handle CRUD operations on table bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
