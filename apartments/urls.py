from django.urls import path

from apartments import views

urlpatterns = [
    path("delete/<int:apt_id>/", views.delete_apartment),
    path("add/", views.add_apartment),
    path("list/", views.get_apartments),
    path("change/<int:apt_id>/", views.change_apartment),
    path("delete/<int:apt_id>/", views.delete_apartment),
]
