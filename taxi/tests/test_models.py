from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class ManufacturerModelTest(TestCase):
    def test_str_returns_name_and_country(self):
        manufacturer = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_ordering_by_name(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual([m.name for m in manufacturers], ["Audi", "BMW"])


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_str_returns_username_and_full_name(self):
        self.assertEqual(str(self.driver), "testuser (John Doe)")

    def test_get_absolute_url_returns_correct_url(self):
        url = self.driver.get_absolute_url()
        expected_url = reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        self.assertEqual(url, expected_url)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Mazda", country="Japan")
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="XYZ00011"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="testpass456",
            license_number="XYZ00022"
        )
        self.car = Car.objects.create(model="CX-5", manufacturer=self.manufacturer)
        self.car.drivers.add(self.driver1, self.driver2)

    def test_str_returns_model_name(self):
        self.assertEqual(str(self.car), "CX-5")

    def test_car_has_multiple_drivers(self):
        self.assertEqual(self.car.drivers.count(), 2)
        self.assertIn(self.driver1, self.car.drivers.all())
        self.assertIn(self.driver2, self.car.drivers.all())
