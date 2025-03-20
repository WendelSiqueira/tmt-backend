import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_many_inventory_entries(n=10):
    language = InventoryLanguage.objects.create(name="Language 1")
    type = InventoryType.objects.create(name="Type 1")
    for i in range(n):
        Inventory.objects.create(
            name=f"Inventory {i}",
            metadata={"key": "value"},
            language=language,
            type=type,
        )
    return Inventory.objects.all()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "offset, limit",
    [
        (0, 5),
        (5, 5),
        (2, 5),
        (0, 10),
    ],
)
def test_inventory_list_pagination(
    api_client, create_many_inventory_entries, offset, limit
):
    url = reverse("inventory-list")
    response = api_client.get(url, {"offset": offset, "limit": limit})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 10
    print(response.data["next"])
    if offset + limit >= 10:
        assert not response.data["next"]
    else:
        assert str(response.data["next"]).endswith(
            f"/inventory/?limit={limit}&offset={offset + limit}"
        )
