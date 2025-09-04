from django.urls import path

from booking import views

urlpatterns = [
    path("", views.BookingAPIView.as_view(), name="booking-create"),
    path("<int:id>/", views.BookingAPIView.as_view(), name="booking-list-delete"),
]
