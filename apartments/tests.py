from http.client import responses

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apartments.models import Apartments


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_apart_create_model():
    apartment = Apartments.objects.create(description="test description", price=10000)

    assert Apartments.objects.count() == 1
    assert apartment.description == "test description"
    assert apartment.price == 10000
    assert apartment.pk is not None


@pytest.mark.django_db
def test_apart_create(client):
    url = reverse("apartments-list")
    data = {"description": "test description", "price": 10000}
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Apartments.objects.count() == 1
    assert response.data["description"] == data["description"]
    assert response.data["price"] == data["price"]
    assert "id" in response.data


@pytest.mark.django_db
def test_apart_create_error(client):
    url = reverse("apartments-list")
    response = client.post(url, {"price": 10000})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["description"] == ["This field is required."]


@pytest.mark.django_db
def test_apart_list(client):
    Apartments.objects.create(description="Apartment 1", price=10000)
    Apartments.objects.create(description="Apartment 2", price=15000)
    response = client.get(reverse("apartments-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[1]["description"] == "Apartment 2"
    assert response.data[1]["price"] == 15000


@pytest.mark.django_db
def test_apart_list_empty(client):
    response = client.get(reverse("apartments-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_apart_patch(client, apartment):
    url = reverse("apartment-details", kwargs={"pk": apartment.pk})
    response = client.patch(url, {"description": "New test description"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["description"] == "New test description"


@pytest.mark.django_db
def test_apart_delete(client, apartment):
    apt_count = Apartments.objects.count()
    url = reverse("apartment-details", kwargs={"pk": apartment.pk})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Apartments.objects.count() == apt_count - 1
    assert not Apartments.objects.filter(pk=apartment.pk).exists()


@pytest.mark.django_db
def test_apart_delete_error(client):
    url = reverse("apartment-details", kwargs={"pk": 10**10})
    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
