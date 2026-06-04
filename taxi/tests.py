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
            password="testpass123",
            license_number="XYZ98765"
        )
        self.client.force_login(self.user)
        self.driver = User.objects.create_user(
            username="johndoe",
            password="password123",
            license_number="ABC12345"
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
    def test_empty_search_returns_all(self):
        """Порожній пошук повертає всі результати"""
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "johndoe")
    def test_no_matching_results(self):
        """Пошук без результатів"""
        response = self.client.get(reverse("taxi:driver-list") + "?q=nonexistent")
        self.assertNotContains(response, "johndoe")
    def test_multiple_matches(self):
        """Додай кілька водіїв з однаковими літерами в імені"""
        User.objects.create_user(username="johnsmith", password="pass", license_number="XYZ11111")
        User.objects.create_user(username="johnny", password="pass", license_number="XYZ22222")
        response = self.client.get(reverse("taxi:driver-list") + "?q=john")
        self.assertContains(response, "johndoe")
        self.assertContains(response, "johnsmith")
        self.assertContains(response, "johnny")
    def test_non_matching_search(self):
        """Переконайся, що неправильний пошук не повертає зайві результати"""
        response = self.client.get(reverse("taxi:driver-list") + "?q=xyz")
        self.assertNotContains(response, "johndoe")
