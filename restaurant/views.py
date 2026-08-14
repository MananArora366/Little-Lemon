from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer

from .forms import BookingForm

# --- CORE DJANGO VIEWS (Modules 2-5) ---

def index(request):
    """Render the Little Lemon home/landing page."""
    # Renders the index.html template (Module 4)
    return render(request, 'index.html', {})

def web_menu_view(request):
    """Traditional view returning HTML for the menu."""
    # Fetch all menu items from the database (Module 3)
    menu_items = Menu.objects.all()
    # Pass the items to the template so it can loop through them (Module 4)
    return render(request, 'menu.html', {'menu_items': menu_items})

def web_book_view(request):
    """Traditional view returning HTML for booking form."""
    if request.method == 'POST':
        # If user submitted the form, grab the data and validate it (Module 5)
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save() # Saves directly to the database
            messages.success(request, "Booking confirmed! We look forward to hosting you.")
            return redirect('restaurant:web-book')
    else:
        # If it's a normal visit (GET request), just show a blank form
        form = BookingForm()
    
    # Render the book.html template, passing the form into it
    return render(request, 'book.html', {'form': form})

# --- ADVANCED API VIEWS (Next Course) ---


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
