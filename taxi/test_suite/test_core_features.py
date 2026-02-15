from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class CoreFeaturesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="john", first_name="John",
            last_name="Doe", license_number="ABC123"
        )

    def test_index_page_loads_successfully(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_car_detail_page_loads(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_driver_detail_page_loads(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
