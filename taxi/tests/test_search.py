from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class SearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver1 = get_user_model().objects.create_user(
            username="alice_driver",
            password="testpassword123",
            license_number="ALI12345",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="bob_driver",
            password="testpassword123",
            license_number="BOB12345",
        )
        self.client.force_login(self.driver1)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota Motor",
            country="Japan",
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW Group",
            country="Germany",
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1,
        )
        self.car3 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2,
        )

    def test_search_manufacturer_by_name(self):
        # Full match / Case insensitive
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "toyota"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.manufacturer1, res.context["manufacturer_list"])
        self.assertNotIn(self.manufacturer2, res.context["manufacturer_list"])

        # Partial match
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "motor"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.manufacturer1, res.context["manufacturer_list"])
        self.assertNotIn(self.manufacturer2, res.context["manufacturer_list"])

        # No match
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": "Audi"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 0)

        # Empty search returns all
        res = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["manufacturer_list"]), 2)

    def test_search_car_by_model(self):
        # Case insensitive match
        res = self.client.get(CAR_LIST_URL, {"model": "camry"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.car1, res.context["car_list"])
        self.assertNotIn(self.car2, res.context["car_list"])
        self.assertNotIn(self.car3, res.context["car_list"])

        # Partial match
        res = self.client.get(CAR_LIST_URL, {"model": "Co"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.car2, res.context["car_list"])
        self.assertNotIn(self.car1, res.context["car_list"])
        self.assertNotIn(self.car3, res.context["car_list"])

        # No match
        res = self.client.get(CAR_LIST_URL, {"model": "Mustang"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 0)

        # Empty search returns all
        res = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["car_list"]), 3)

    def test_search_driver_by_username(self):
        # Exact match / Case insensitive
        res = self.client.get(DRIVER_LIST_URL, {"username": "ALICE"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.driver1, res.context["driver_list"])
        self.assertNotIn(self.driver2, res.context["driver_list"])

        # Partial match
        res = self.client.get(DRIVER_LIST_URL, {"username": "bob"})
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.driver2, res.context["driver_list"])
        self.assertNotIn(self.driver1, res.context["driver_list"])

        # Shared substring
        res = self.client.get(DRIVER_LIST_URL, {"username": "driver"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 2)

        # No match
        res = self.client.get(DRIVER_LIST_URL, {"username": "charlie"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["driver_list"]), 0)
