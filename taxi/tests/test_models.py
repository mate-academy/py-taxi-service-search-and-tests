from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        self.assertEqual(str(manufacturer), "Ford USA")

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Mustang", manufacturer=manufacturer)
        self.assertEqual(str(car), "Mustang")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )
        self.assertEqual(str(driver), "johndoe (John Doe)")

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="driver1",
            license_number="XYZ98765"
        )
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": driver.pk})
        self.assertEqual(driver.get_absolute_url(), expected_url)

    def test_manufacturer_ordering(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")

        manufacturers = list(Manufacturer.objects.all())

        self.assertEqual(manufacturers[0].name, "Audi")
        self.assertEqual(manufacturers[1].name, "BMW")
        self.assertEqual(manufacturers[2].name, "Toyota")
