import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_inventory_list(api_client):
    language = InventoryLanguage.objects.create(name="Language 1")
    type = InventoryType.objects.create(name="Type 1")
    Inventory.objects.create(
        name="Inventory 1",
        metadata={"key": "value"},
        language=language,
        type=type,
        created_at="2025-01-01",
    )
    later_date_inventory = Inventory.objects.create(
        name="Inventory 2",
        metadata={"key": "value"},
        language=language,
        type=type,
        created_at="2025-01-02",
    )
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    later_date_inventory.created_at = tomorrow
    later_date_inventory.save(update_fields=["created_at"])
    url = reverse("inventory-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    response = api_client.get(
        url, {"created_at": datetime.datetime.now().strftime("%Y-%m-%d")}
    )
    assert len(response.data) == 2
    response = api_client.get(url, {"created_at": tomorrow.strftime("%Y-%m-%d")})
    assert len(response.data) == 1


@pytest.mark.django_db
def test_inventory_list_invalid_date_filter(api_client):
    url = reverse("inventory-list")
    response = api_client.get(url, {"created_at": "invalid-date"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
