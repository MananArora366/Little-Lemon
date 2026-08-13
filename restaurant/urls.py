from django.urls import path
from . import views

# This routes URLs specifically for the restaurant app
urlpatterns = [
    # When the user visits the root of this app, trigger the 'index' view
    path('', views.index, name='index'),
]
