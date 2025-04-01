from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="john_doe",
            license_number="ABC12312"
        )
        self.driver2 = Driver.objects.create(
            username="jane_smith",
            license_number="XYZ45612"
        )

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda")

        self.car1 = Car.objects.create(
            model="Toyota Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Honda Civic",
            manufacturer=self.manufacturer2
        )

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?q=john"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertNotContains(response, self.driver2.username)

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list") + "?q=Corolla"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?q=Toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
