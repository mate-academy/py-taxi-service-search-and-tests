from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_model_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden",
        )
        self.assertEqual(
            str(manufacturer),
            "Volvo Sweden"
        )

    def test_driver_model_str(self):
        driver = get_user_model().objects.create(
            username="frodo_torba",
            password="test123!",
            first_name="Frodo",
            last_name="Baggins",
        )
        self.assertEqual(
            str(driver),
            "frodo_torba (Frodo Baggins)"
        )

    def test_car_model_str(self):
        driver = get_user_model().objects.create(
            username="frodo_torba",
            password="test123!",
            first_name="Frodo",
            last_name="Baggins",
        )
        manufacturer = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden",
        )
        car = Car.objects.create(
            model="V50",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        self.assertEqual(
            str(car),
            "V50"
        )

    def test_create_driver_with_license(self):
        username = "frodo_torba"
        password = "test123!"
        license_number = "QWE12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number,
        )
        self.assertEqual(
            driver.username,
            username
        )
        self.assertEqual(
            driver.license_number,
            license_number
        )
        self.assertTrue(
            driver.check_password(password)
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create(
            username="frodo_torba",
            password="test123!",
            first_name="Frodo",
            last_name="Baggins",
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(
            driver.get_absolute_url(),
            expected_url
        )
