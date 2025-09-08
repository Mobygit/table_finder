from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_selection, name='menu_selection'),
    path('reserve/', views.reservation_form, name='reservation_form'),
    path('preview/', views.reservation_preview, name='reservation_preview'),
    path('success/', views.booking_success, name='success'),
]
