from django.urls import path
from .views import (
    CreateBookingView,
    UserBookingsView,
    ServiceProviderBookingsView,
    AvailableSlotsView,
    UpdateBookingStatusView,
)

urlpatterns = [
    path('create/', CreateBookingView.as_view(), name='create-booking'),
    path('my-bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('provider-bookings/', ServiceProviderBookingsView.as_view(), name='provider-bookings'),
    path('slots/', AvailableSlotsView.as_view(), name='available-slots'),
    path('update-status/<int:pk>/', UpdateBookingStatusView.as_view(), name='update-booking-status'),
]
