from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ManufacturerModelTests(TestCase):
    def test_str_returns_name_and_country(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )

        self.assertEqual(str(manufacturer), "Honda Japan")


class DriverModelTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="johndoe",
            password="Strong-password-123",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )

    def test_str_returns_username_and_full_name(self):
        self.assertEqual(str(self.driver), "johndoe (John Doe)")

    def test_get_absolute_url_returns_driver_detail_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            f"/drivers/{self.driver.pk}/",
        )

    def test_driver_can_be_created_with_license_number(self):
        self.assertEqual(self.driver.license_number, "ABC12345")


class CarModelTests(TestCase):
    def test_str_returns_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        car = Car.objects.create(model="Civic", manufacturer=manufacturer)

        self.assertEqual(str(car), "Civic")
