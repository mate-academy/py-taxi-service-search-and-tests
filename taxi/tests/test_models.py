from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        cls.driver = get_user_model().objects.create_user(
            username="john.doe",
            password="test12345",
            first_name="John",
            last_name="Doe",
            license_number="JOH12345",
        )

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Ford USA")

    def test_manufacturers_are_ordered_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        self.assertEqual(
            list(Manufacturer.objects.values_list("name", flat=True)),
            ["BMW", "Ford", "Toyota"],
        )

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "john.doe (John Doe)")

    def test_driver_is_created_with_license_number(self):
        self.assertEqual(self.driver.license_number, "JOH12345")
        self.assertTrue(self.driver.check_password("test12345"))

    def test_driver_get_absolute_url(self):
        self.assertEqual(
            self.driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk}),
        )

    def test_car_str(self):
        car = Car.objects.create(model="Focus", manufacturer=self.manufacturer)
        self.assertEqual(str(car), "Focus")
