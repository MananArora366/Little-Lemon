from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """
    A simple view that takes a web request and returns a basic HTTP response.
    This will replace the default Django rocket page.
    """
    return HttpResponse("Welcome to Little Lemon Restaurant!")
