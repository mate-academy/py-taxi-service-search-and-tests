from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="testname",
                                                   country="testcountry")
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}")

    def test_driver_str(self):
        driver = get_user_model().objects.create(username="testusername",
                                                 password="testpassword",
                                                 first_name="testfirstname",
                                                 last_name="testlastname")

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create(username="testusername",
                                                 password="testpassword",
                                                 first_name="testfirstname",
                                                 last_name="testlastname")

        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_create_driver_with_license_number(self):
        username = "testusername"
        password = "testpassword"
        license_number = "AAA12312"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="testname",
            country="testcountry"
        )
        car = Car.objects.create(model="testmodel", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)
