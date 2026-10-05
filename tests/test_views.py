from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Driver, Manufacturer


class ViewsTestCases(TestCase):
    def test_manufacturer_search_by_name(self):
        user = Driver.objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12345"
        )
        self.client.force_login(user)
        manufacturer_1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Toyota"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, manufacturer_1.name)
        self.assertNotContains(response, manufacturer_2.name)

    def test_car_search_by_model(self):
        user = Driver.objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12345"
        )
        self.client.force_login(user)
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car_1 = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer
        )
        car_2 = Car.objects.create(
            model="Corolla",
            manufacturer=manufacturer
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Camry"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, car_1.model)
        self.assertNotContains(response, car_2.model)

    def test_driver_search_by_username(self):
        user = Driver.objects.create_user(
            username="testuser",
            password="testpassword",
            license_number="ABC12445"
        )
        self.client.force_login(user)
        driver_1 = Driver.objects.create_user(
            username="driver1",
            password="password1",
            license_number="DEF67890"
        )
        driver_2 = Driver.objects.create_user(
            username="driver2",
            password="password2",
            license_number="ABC13345"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver_1.username)
        self.assertNotContains(response, driver_2.username)
