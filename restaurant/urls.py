from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    path('', views.index, name='index'),
    path('web-menu/', views.web_menu_view, name='web-menu'),
    path('web-menu/<int:pk>/', views.web_menu_item_view, name='web-menu-item'),
    path('web-book/', views.web_book_view, name='web-book'),
    path('menu/', views.MenuItemsView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-detail'),
]
