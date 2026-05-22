import pytest
from django.urls import reverse
from django.core.exceptions import ValidationError

from taxi.forms import validate_license_number
from taxi.models import Manufacturer, Car, Driver


@pytest.mark.django_db
def test_driver_search(client):
    user = Driver.objects.create_user(
        username="admin",
        password="test12345",
        license_number="ADM12345",
    )
    client.force_login(user)

    Driver.objects.create_user(
        username="john",
        password="test12345",
        license_number="JOH12345",
    )
    Driver.objects.create_user(
        username="mike",
        password="test12345",
        license_number="MIK12345",
    )

    response = client.get(reverse("taxi:driver-list"), {"username": "john"})

    assert response.status_code == 200
    assert "john" in response.content.decode()
    assert "mike" not in response.content.decode()


@pytest.mark.django_db
def test_car_search(client):
    user = Driver.objects.create_user(
        username="admin",
        password="test12345",
        license_number="ADM12345",
    )
    client.force_login(user)

    manufacturer = Manufacturer.objects.create(name="BMW", country="Germany")
    Car.objects.create(model="X5", manufacturer=manufacturer)
    Car.objects.create(model="A6", manufacturer=manufacturer)

    response = client.get(reverse("taxi:car-list"), {"model": "X5"})

    assert response.status_code == 200
    assert "X5" in response.content.decode()
    assert "A6" not in response.content.decode()


@pytest.mark.django_db
def test_manufacturer_search(client):
    user = Driver.objects.create_user(
        username="admin",
        password="test12345",
        license_number="ADM12345",
    )
    client.force_login(user)

    Manufacturer.objects.create(name="BMW", country="Germany")
    Manufacturer.objects.create(name="Audi", country="Germany")

    response = client.get(reverse("taxi:manufacturer-list"), {"name": "BMW"})

    assert response.status_code == 200
    assert "BMW" in response.content.decode()
    assert "Audi" not in response.content.decode()


def test_valid_license_number():
    license_number = "ABC12345"

    assert validate_license_number(license_number) == license_number


@pytest.mark.parametrize(
    "license_number",
    [
        "ABC123",
        "abc12345",
        "ABC12AAA",
    ],
)
def test_invalid_license_number(license_number):
    with pytest.raises(ValidationError):
        validate_license_number(license_number)
