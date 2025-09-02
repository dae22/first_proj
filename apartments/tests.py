import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apartments.models import Apartments


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_apart_create():
    apartment = Apartments.objects.create(description="test description", price=10000)

    assert Apartments.objects.count() == 1
    assert apartment.description == "test description"
    assert apartment.price == 10000
    assert apartment.pk is not None


@pytest.mark.django_db
def test_aparts_list(client):
    Apartments.objects.create(description="Apartment 1", price=10000)
    Apartments.objects.create(description="Apartment 2", price=15000)
    response = client.get(reverse("apartments-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[1]["description"] == "Apartment 2"
    assert response.data[1]["price"] == 15000


@pytest.mark.django_db
def test_apartment_delete_1(client):
    apartment = Apartments.objects.create(description="To delete", price=5000)
    apt_count = Apartments.objects.count()

    url = reverse("apartment-details", kwargs={"pk": apartment.pk})
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Apartments.objects.count() == apt_count - 1
    assert not Apartments.objects.filter(pk=apartment.pk).exists()


@pytest.mark.django_db
def test_apartment_delete_2(client):
    url = reverse("apartment-details", kwargs={"pk": 10**10})
    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
