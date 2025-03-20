from unittest.mock import ANY

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order, OrderTag


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_orders():
    language = InventoryLanguage.objects.create(name="Language 1")
    type = InventoryType.objects.create(name="Type 1")
    order_tag_1 = OrderTag.objects.create(name="Tag 1")
    order_tag_2 = OrderTag.objects.create(name="Tag 2")

    inventory = Inventory.objects.create(
        name="Inventory 1",
        metadata={"key": "value"},
        language=language,
        type=type,
    )
    order = Order.objects.create(
        pk=1,
        inventory=inventory,
        start_date="2025-01-01",
        embargo_date="2025-02-01",
    )
    order.tags.set([order_tag_1, order_tag_2])
    order_2 = Order.objects.create(
        pk=2,
        inventory=inventory,
        start_date="2025-01-01",
        embargo_date="2025-02-01",
    )
    order_2.tags.set([order_tag_2])
    print(order_2.pk, order_2.tags.all())


@pytest.mark.django_db
@pytest.mark.parametrize(
    "pk, expected_response",
    [
        (
            1,
            [
                {"id": ANY, "name": "Tag 1", "is_active": True},
                {"id": 2, "name": "Tag 2", "is_active": True},
            ],
        ),
        (2, [{"id": ANY, "name": "Tag 2", "is_active": True}]),
    ],
)
def test_order_tag_by_order(api_client, create_orders, pk, expected_response):
    url = reverse("order-tag-detail", kwargs={"pk": pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_response
