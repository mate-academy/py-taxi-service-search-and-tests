from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsStr(TestCase):
    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer(name="testname", country="testcountry")
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}",
        )

    def test_driver_model_str(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            last_name="testlastname",
            first_name="testfirstname",
            license_number="testlicense_number",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12345",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_car_model_str(self):
        car = Car(
            model="testmodel",
            manufacturer=Manufacturer(name="testmanufacturer"),
        )
        self.assertEqual(str(car), f"{car.model}")
