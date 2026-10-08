from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer

from .forms import BookingForm

# --- CORE DJANGO VIEWS (Modules 2-5) ---

def index(request):
    """Render the Little Lemon home/landing page."""
    # Renders the index.html template (Module 4)
    return render(request, 'index.html', {})

def web_menu_view(request):
    """Traditional view returning HTML for the menu list (filtered & ordered)."""
    # Only fetch items that are in stock, sorted alphabetically by title
    menu_items = Menu.objects.filter(inventory__gt=0).order_by('title')
    # Pass the items to the template so it can loop through them (Module 4)
    return render(request, 'menu.html', {'menu_items': menu_items})

def web_menu_item_view(request, pk):
    """Traditional view returning HTML for a single menu item with 404 handling."""
    # get_object_or_404 raises Http404 (404 status) instead of unhandled DoesNotExist (500 crash)
    menu_item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {'menu_item': menu_item})

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
    """API view to list all menu items (public) or create a new menu item (authenticated)."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """API view to get a menu item (public) or update/delete (authenticated)."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """ModelViewSet to handle CRUD operations on table bookings (requires authentication)."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
