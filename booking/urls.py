from django.urls import path

from booking import views

urlpatterns = [
    path("add/", views.add_booking),
    path("check_booking/<int:apt_id>/", views.get_booking),
    path("delete/<int:booking_id>/", views.delete_booking),
]
