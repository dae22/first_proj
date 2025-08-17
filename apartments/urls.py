from django.urls import path

from apartments import views

urlpatterns = [
    path("delete/<int:apt_id>/", views.delete_apartment),
    path("add/", views.add_apartment),
    path("list/", views.ApartmentsAPIView.as_view()),
]
