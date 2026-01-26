from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", password="pass12345", license_number="ABC12345"
        )
        self.client.login(username="tester", password="pass12345")

    def test_driver_search_by_username(self):
        Driver.objects.create_user(username="johnny",
                                   password="pass12345",
                                   license_number="AAA12345")
        Driver.objects.create_user(username="mike",
                                   password="pass12345",
                                   license_number="BBB12345")

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "john"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "johnny")
        self.assertNotContains(response, "mike")

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        Car.objects.create(model="Focus", manufacturer=manufacturer)
        Car.objects.create(model="Fiesta", manufacturer=manufacturer)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "foc"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Focus")
        self.assertNotContains(response, "Fiesta")

    def test_manufacturer_search_by_name(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "for"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Ford")
        self.assertNotContains(response, "Toyota")
