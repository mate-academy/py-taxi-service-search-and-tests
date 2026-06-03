from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.models import Manufacturer, Car


User = get_user_model()


class DriverModelTest(TestCase):
    def test_license_number_validation(self):
        driver = User.objects.create_user(
            username="test_driver",
            password="password123",
            license_number="ABC12345"
        )
        self.assertEqual(driver.license_number, "ABC12345")


class SearchViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

        self.driver = User.objects.create_user(
            username="johndoe",
            password="password123",
            license_number="ABC12345"  # <-- додай це поле
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )

    def test_driver_search(self):
        response = self.client.get(reverse("taxi:driver-list") + "?q=john")
        self.assertContains(response, "johndoe")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=Cam")
        self.assertContains(response, "Camry")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?q=Toy"
        )
        self.assertContains(response, "Toyota")
