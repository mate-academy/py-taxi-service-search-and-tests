from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


# Create your tests here.
class ModelsTest(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = (Manufacturer.objects.create(name="test",
                                                    country="test"))
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self) -> None:
        driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name}"
                         f" {driver.last_name})")

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345"
        )
        car = Car.objects.create(
            model="m3",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(str(car), f"{car.model}")

    def test_license_number(self) -> None:
        driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver.license_number), "ABC12345")

    def test_get_absolute_url(self) -> None:
        driver = get_user_model().objects.create(
            username="test",
            email="<ilaruslanovich7@gmail.com>",
            password="<Gitarist2005>",
            first_name="test",
            last_name="test",
            license_number="ABC12345"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)
