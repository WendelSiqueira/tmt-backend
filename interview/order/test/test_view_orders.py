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
def test_order_list_without_filters(api_client, create_order):
    url = reverse("order-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter_params, expected_count",
    [
        ({"start_date": "2025-01-01"}, 1),
        ({"start_date": "2025-02-01"}, 0),
        ({"embargo_date": "2025-02-01"}, 1),
        ({"embargo_date": "2025-01-01"}, 0),
        ({"start_date": "2025-01-01", "embargo_date": "2025-02-01"}, 1),
        ({"start_date": "2025-01-02", "embargo_date": "2025-01-15"}, 0),
    ],
)
def test_order_list(api_client, create_order, filter_params, expected_count):
    url = reverse("order-list")
    response = api_client.get(url, filter_params)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count
