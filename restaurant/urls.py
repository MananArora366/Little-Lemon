from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('web-menu/', views.web_menu_view, name='web-menu'),
    path('web-book/', views.web_book_view, name='web-book'),
    path('menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
]
