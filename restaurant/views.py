from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer

from .forms import BookingForm

def index(request):
    """Render the Little Lemon home/landing page."""
    return render(request, 'index.html', {})

def web_menu_view(request):
    """Traditional view returning HTML for the menu."""
    menu_items = Menu.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})

def web_book_view(request):
    """Traditional view returning HTML for booking form."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BookingForm()
    return render(request, 'book.html', {'form': form})


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
