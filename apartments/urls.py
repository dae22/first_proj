from django.urls import path

from apartments import views

urlpatterns = [
    path("", views.ApartmentsAPI.as_view()),
    path("<int:pk>/", views.ApartmentsAPI.as_view()),
]
