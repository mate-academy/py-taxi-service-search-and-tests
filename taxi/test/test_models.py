from django.contrib.auth import get_user, get_user_model
from django.template.defaultfilters import first
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacture_model_str(self) -> None:
        manufacture = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEquals(
            str(manufacture),
            f"{manufacture.name} {manufacture.country}"
        )

    def test_driver_model_str(self) -> None:
        driver = get_user_model().objects.create(
            username="test_name",
            first_name="first_name",
            last_name="last_name",
            password="test_password_12345",
            license_number="ANC12345"
        )
        self.assertEquals(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_model_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )

        self.assertEquals(str(car), car.model)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(
            username="test_name",
            first_name="first_name",
            last_name="last_name",
            password="test_password_12345",
            license_number="ANC12345"
        )
        self.assertEquals(driver.get_absolute_url(), f"/drivers/{driver.pk}/")

    def test_driver_if_add_custom_fields(self):
        first_name = "first_name"
        last_name = "last_name"
        license_number = "ANC12345"

        driver = get_user_model().objects.create(
            username="test_name",
            first_name=first_name,
            last_name=last_name,
            password="test_password_12345",
            license_number=license_number
        )
        self.assertEquals(driver.license_number, license_number)
        self.assertEquals(driver.first_name, first_name)
        self.assertEquals(driver.last_name, last_name)
