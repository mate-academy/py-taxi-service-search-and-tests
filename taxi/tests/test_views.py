from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="testCountry"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="test_driver",
            password="test123"
        )

        self.client.login(username="test_driver", password="test123")

    def test_manufacturer_list_view_connection(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_list_view_connection(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_list_view_connection(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_list_detail_connection(self):
        url = reverse("taxi:car-detail", args=[self.car.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_list_detail_connection(self):
        url = reverse("taxi:driver-detail", args=[self.driver.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_create_connection(self):
        url = reverse("taxi:manufacturer-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_create_connection(self):
        url = reverse("taxi:car-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_create_connection(self):
        url = reverse("taxi:driver-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_update_connection(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_update_connection(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_license_update_connection(self):
        url = reverse("taxi:driver-update", args=[self.driver.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_manufacturer_delete_connection(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_car_delete_connection(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_driver_license_delete_connection(self):
        url = reverse("taxi:driver-delete", args=[self.driver.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
