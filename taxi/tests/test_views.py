from django.test import Client
from django.urls import reverse
import pytest

from taxi.models import (
    Manufacturer,
    Car,
    Driver
)


@pytest.mark.parametrize(
    "url",
    [
        pytest.param(
            reverse("taxi:manufacturer-list"),
            id="manufacturer list"
        ),
        pytest.param(
            reverse("taxi:manufacturer-create"),
            id="manufacturer create"
        ),
        pytest.param(reverse("taxi:car-list"), id="car list"),
        pytest.param(reverse("taxi:car-create"), id="car create"),
        pytest.param(reverse("taxi:driver-list"), id="driver list"),
        pytest.param(reverse("taxi:driver-create"), id="driver create"),
    ]
)
def test_login_required(url):
    client = Client()
    res = client.get(url)
    assert res.status_code != 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url",
    [
        pytest.param("taxi:manufacturer-update", id="manufacturer update"),
        pytest.param("taxi:manufacturer-delete", id="manufacturer delete"),
        pytest.param("taxi:car-detail", id="car detail"),
        pytest.param("taxi:car-update", id="car update"),
        pytest.param("taxi:car-delete", id="car delete"),
        pytest.param("taxi:driver-detail", id="driver detail"),
        pytest.param("taxi:driver-update", id="driver update license"),
        pytest.param("taxi:driver-delete", id="driver delete"),
    ]
)
def test_login_required_with_pk(url):
    manufacturer = Manufacturer.objects.create(
        name="Test_name",
        country="country"
    )
    Car.objects.create(model="Test", manufacturer=manufacturer)
    Driver.objects.create_user(
        username="Test_name",
        password="Test_1234",
        license_number="ABC12345"
    )
    url = reverse(url, kwargs={"pk": 1})
    client = Client()
    res = client.get(url)
    assert res.status_code == 302
