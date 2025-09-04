import pytest
from rest_framework.test import APIClient

from apartments.models import Apartments


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def apartment():
    return Apartments.objects.create(description="test description", price=10000)
