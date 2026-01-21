from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Car, Manufacturer
from django.contrib.auth import get_user_model


class TaxiViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan")
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer)
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345"
        )

    def test_car_list_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")

    def test_driver_detail_view(self):
        self.client.login(username="testuser", password="12345")
        self.driver = Driver.objects.create(
            username="driveruser",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe"
        )
        response = self.client.get(reverse("taxi:driver-detail",
                                           args=[self.driver.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driveruser")
