from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class PublicTestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass",
            license_number="12345"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        cls.car = Car.objects.create(
            model="Camry",
            manufacturer=cls.manufacturer
        )
        cls.car.drivers.set([cls.driver])

        cls.URLS = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=[cls.manufacturer.id]),
            reverse("taxi:manufacturer-delete", args=[cls.manufacturer.id]),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=[cls.car.id]),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=[cls.car.id]),
            reverse("taxi:car-delete", args=[cls.car.id]),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=[cls.driver.id]),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", args=[cls.driver.id]),
            reverse("taxi:driver-delete", args=[cls.driver.id]),
        ]

    def test_login_required(self):
        for url in self.URLS:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)

    def test_retrieve_view(self):
        self.client.force_login(self.driver)
        for url in self.URLS:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
