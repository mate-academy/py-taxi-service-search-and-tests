import pytest
from django.contrib.auth import get_user_model
from django.db.models import Model

from taxi.models import Manufacturer, Car

pytestmark = pytest.mark.django_db


def test_manufacturer_str():
    manufacturer = Manufacturer.objects.create(
        name="Mercedes",
        country="Germany"
    )
    assert str(manufacturer) == f"{manufacturer.name} {manufacturer.country}"


def test_driver_str():
    driver = get_user_model().objects.create(
        username="john_doe",
        first_name="John",
        last_name="Doe",
        password="test123",
        license_number="AAA12345"
    )
    assert str(driver) == (f"{driver.username} "
                           f"({driver.first_name} {driver.last_name})")


def test_car_str():
    manufacturer = Manufacturer.objects.create(
        name="Mercedes",
        country="Germany"
    )
    driver = get_user_model().objects.create(
        username="john_doe",
        first_name="John",
        last_name="Doe",
        password="test123",
        license_number="AAA12345"
    )
    car = Car.objects.create(
        model="AMG",
        manufacturer=manufacturer,
    )
    car.drivers.add(driver)
    assert str(car) == car.model
