from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        self.driver = get_user_model().objects.create_user(
            username="john.doe",
            password="Test12345!",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345",
        )

    def test_manufacturer_str(self) -> None:
        self.assertEqual(str(self.manufacturer), "Lincoln USA")

    def test_driver_str(self) -> None:
        self.assertEqual(str(self.driver), "john.doe (John Doe)")

    def test_car_str(self) -> None:
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        self.assertEqual(str(car), "Continental")

    def test_create_driver_with_license_number(self) -> None:
        self.assertEqual(self.driver.license_number, "ABC12345")
        self.assertNotEqual(self.driver.password, "Test12345!")
        self.assertTrue(self.driver.check_password("Test12345!"))

    def test_driver_get_absolute_url(self) -> None:
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )

    def test_manufacturers_are_ordered_by_name(self) -> None:
        Manufacturer.objects.create(name="Audi", country="Germany")
        names = list(Manufacturer.objects.values_list("name", flat=True))
        self.assertEqual(names, ["Audi", "Lincoln"])
