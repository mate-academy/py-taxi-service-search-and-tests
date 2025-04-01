from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

Driver = get_user_model()


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_manufacturer_get_absolute_url(self):
        manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="test_country"
        )
        expected_url = reverse(
            "taxi:manufacturer-detail"
            , kwargs={"pk": manufacturer.pk}
        )
        self.assertEqual(manufacturer.get_absolute_url(), expected_url)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_car_get_absolute_url(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car = Car.objects.create(model="test_model", manufacturer=manufacturer)
        expected_url = reverse("taxi:car-detail", kwargs={"pk": car.pk})
        self.assertEqual(car.get_absolute_url(), expected_url)

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="test_name",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_get_absolute_url(self):
        driver = Driver.objects.create(
            username="TestNme"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_create_driver_with_license_number(self):
        username = "test_name"
        first_name = "test_first"
        last_name = "test_last"
        password = "test_password"
        license_number = "test_license"

        driver = Driver.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.first_name, first_name)
        self.assertEqual(driver.last_name, last_name)
        self.assertEqual(driver.license_number, license_number)
        # password check
        self.assertTrue(driver.check_password(password), password)
