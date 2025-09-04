from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from booking.models import Booking


@pytest.mark.django_db
def test_booking_model(apartment):
    booking = Booking.objects.create(apartment=apartment, start_date="2025-09-03", end_date="2025-09-10")

    assert Booking.objects.count() == 1
    assert booking.start_date == "2025-09-03"
    assert booking.end_date == "2025-09-10"
    assert booking.apartment == apartment
    assert booking.pk is not None


@pytest.mark.django_db
def test_booking_create(client, apartment):
    data = {"apartment_id": apartment.pk, "start_date": "2025-09-03", "end_date": "2025-09-10"}
    url = reverse("booking-create")
    response = client.post(url, data)
    booking = Booking.objects.first()

    assert response.status_code == status.HTTP_201_CREATED
    assert Booking.objects.count() == 1
    assert booking.apartment == apartment
    assert booking.start_date == date.fromisoformat("2025-09-03")
    assert booking.end_date == date.fromisoformat("2025-09-10")
    assert booking.pk is not None


@pytest.mark.django_db
def test_booking_create_no_field(client, apartment):
    data = {"apartment": apartment, "end_date": "2025-09-10"}
    url = reverse("booking-create")
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["start_date"] == ["This field is required."]


@pytest.mark.django_db
def test_booking_create_bad_type(client, apartment):
    data = {"apartment": apartment, "start_date": "2025-12-12", "end_date": "data"}
    url = reverse("booking-create")
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Date has wrong format" in response.json()["end_date"][0]


@pytest.mark.django_db
def test_booking_create_cross(client, apartment):
    Booking.objects.create(apartment=apartment, start_date="2025-09-03", end_date="2025-09-10")
    data = {"apartment_id": apartment.pk, "start_date": "2025-09-03", "end_date": "2025-09-10"}
    url = reverse("booking-create")
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cross" in response.json()["non_field_errors"][0].lower()


@pytest.mark.django_db
def test_booking_list(client, apartment):
    Booking.objects.create(apartment=apartment, start_date="2025-09-03", end_date="2025-09-10")
    Booking.objects.create(apartment=apartment, start_date="2025-09-11", end_date="2025-09-20")
    url = reverse("booking-list-delete", kwargs={"id": apartment.pk})
    response = client.get(url)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 2
    assert response_data[0]["start_date"] == "2025-09-03"
    assert response_data[1]["end_date"] == "2025-09-20"


@pytest.mark.django_db
def test_booking_list_error(client):
    url = reverse("booking-list-delete", kwargs={"id": 999})
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error"] == "Booking not found"


@pytest.mark.django_db
def test_booking_delete(client, apartment):
    booking = Booking.objects.create(apartment=apartment, start_date="2025-09-03", end_date="2025-09-10")
    cnt = Booking.objects.count()
    url = reverse("booking-list-delete", kwargs={"id": booking.pk})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Booking.objects.count() == cnt - 1


@pytest.mark.django_db
def test_booking_delete_error(client):
    url = reverse("booking-list-delete", kwargs={"id": 999})
    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No Booking matches the given query."
