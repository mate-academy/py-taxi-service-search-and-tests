from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class AdminTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.client.login(username="admin", password="admin123")
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer

        )
        self.driver = Driver.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="test123",
            license_number="123456"
        )

    def test_driver_list_view(self):
        response = self.client.get(reverse("admin:taxi_driver_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_driver_detail_view(self):
        response = self.client.get(reverse(
            "admin:taxi_driver_change",
            args=(self.driver.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_car_list_view(self):
        response = self.client.get(reverse("admin:taxi_car_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_car_detail_view(self):
        response = self.client.get(reverse(
            "admin:taxi_car_change",
            args=(self.car.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view(self):
        response = (self.client.get
                    (reverse("admin:taxi_manufacturer_changelist")))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_detail_view(self):
        response = self.client.get(reverse(
            "admin:taxi_manufacturer_change",
            args=(self.manufacturer.id,))
        )
        self.assertEqual(response.status_code, 200)
