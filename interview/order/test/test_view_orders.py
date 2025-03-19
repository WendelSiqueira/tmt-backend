import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_order():
    language = InventoryLanguage.objects.create(name="Language 1")
    type = InventoryType.objects.create(name="Type 1")
    inventory = Inventory.objects.create(
        name="Inventory 1",
        metadata={"key": "value"},
        language=language,
        type=type,
    )
    return Order.objects.create(
        inventory=inventory,
        start_date="2025-01-01",
        embargo_date="2025-02-01",
    )


@pytest.mark.django_db
def test_deactivate_order_view_invalid_pk(api_client):
    response = api_client.put("/orders/deactivate", {"pk": "invalid"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_deactivate_order_view_activate(api_client, create_order):
    response = api_client.put(f"/orders/{create_order.id}/activate")
    assert response.status_code == status.HTTP_200_OK
    create_order.refresh_from_db()
    assert create_order.is_active is True


@pytest.mark.django_db
def test_deactivate_order_view_deactivate(api_client, create_order):
    response = api_client.put(f"/orders/{create_order.id}/deactivate")
    assert response.status_code == status.HTTP_200_OK
    create_order.refresh_from_db()
    assert create_order.is_active is False
