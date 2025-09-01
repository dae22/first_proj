from django.urls import path

from booking import views

urlpatterns = [
    path("", views.BookingAPIView.as_view()),
    path("<int:apartment_id>/", views.BookingAPIView.as_view()),
]
