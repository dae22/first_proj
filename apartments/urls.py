from django.urls import path

from apartments import views

urlpatterns = [
    path("", views.ApartmentsAPI.as_view(), name="apartments-list"),
    path("<int:pk>/", views.ApartmentsAPI.as_view(), name="apartment-details"),
]
