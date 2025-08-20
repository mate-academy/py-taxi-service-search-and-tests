from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicViewsTest(TestCase):
    def test_login_required(self):
        res_car = self.client.get(CAR_URL)
        res_manufacturer = self.client.get(MANUFACTURER_URL)
        res_driver = self.client.get(DRIVER_URL)
        self.assertNotEqual(res_car.status_code, 200)
        self.assertNotEqual(res_manufacturer.status_code, 200)
        self.assertNotEqual(res_driver.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC4567"
        )

        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="test",
            license_number="ABC456"
        )

    def test_manufacturer_list_loads(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_loads(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_driver_list_loads(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search_by_name(self):
        response = self.client.get(MANUFACTURER_URL, {"name": "Toyota"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "BMW")

    def test_car_search_by_model(self):
        response = self.client.get(CAR_URL, {"model": "Camry"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Camry")
        self.assertNotContains(response, "X5")

    def test_driver_search_by_username(self):
        response = self.client.get(DRIVER_URL, {"username": "driver1"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_manufacturer_list_template(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_car_list_template(self):
        response = self.client.get(CAR_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list_template(self):
        response = self.client.get(DRIVER_URL)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
