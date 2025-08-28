from django.urls import path

from booking import views

urlpatterns = [
    path("add/", views.BookingAPIView.as_view(), name="add"),
    path(
        "check_booking/<int:apt_id>/",
        views.BookingAPIView.as_view(),
        name="check_booking",
    ),
    path("delete/<int:booking_id>/", views.BookingAPIView.as_view(), name="delete"),
]
