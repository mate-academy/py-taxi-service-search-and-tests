from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


CAR_FORMAT_URL = reverse("taxi:car-list")
DRIVER_FORMAT_URL = reverse("taxi:driver-list")
MANUFACTURER_FORMAT_URL = reverse("taxi:manufacturer-list")


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CAR_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = (get_user_model()
                     .objects.create_user(username="tester",
                                          password="pass",
                                          license_number="test123"))
        self.client.force_login(self.user)
        self.match = (get_user_model()
                      .objects.create_user(username="john_doe",
                                           password="p",
                                           license_number="test1234"))
        self.nonmatch = (get_user_model()
                         .objects.create_user(username="anna",
                                              password="p",
                                              license_number="test12345"))

    def test_search_by_username_returns_matching(self):
        res = self.client.get(DRIVER_FORMAT_URL, {"username": "john"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "john_doe")
        self.assertNotContains(res, "anna")

    def test_pagination(self):
        for i in range(8):
            (get_user_model()
             .objects.create_user(username=f"m{i}",
                                  password="pass",
                                  license_number=f"{i}test123"))
        res = self.client.get(DRIVER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context.get("is_paginated"))
        objects = res.context["driver_list"]
        self.assertEqual(len(objects), 5)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.manufacturer = (Manufacturer.objects.
                             create(name="test_name",
                                    country="test_country"))
        self.client = Client()
        self.match = Car.objects.create(
            model="Toyota",
            manufacturer=self.manufacturer,
        )
        self.nonmatch = Car.objects.create(
            model="Mitsubishi",
            manufacturer=self.manufacturer,
        )
        self.user = (get_user_model()
                     .objects.create_user(username="tester",
                                          password="pass",
                                          license_number="test123"))
        self.client.force_login(self.user)

    def test_search_by_model_returns_matching(self):
        res = self.client.get(CAR_FORMAT_URL, data={"model": "Toyota"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Mitsubishi")

    def test_pagination(self):
        for i in range(8):
            Car.objects.create(model=f"m{i}", manufacturer=self.manufacturer)
        res = self.client.get(CAR_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context.get("is_paginated"))
        objects = res.context["car_list"]
        self.assertEqual(len(objects), 5)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.match = Manufacturer.objects.create(name="toyota",
                                                 country="test_country")
        self.nonmatch = Manufacturer.objects.create(name="mitsubishi",
                                                    country="test_country")
        self.user = (get_user_model()
                     .objects.create_user(username="tester",
                                          password="pass",
                                          license_number="test123"))
        self.client.force_login(self.user)

    def test_search_by_name_returns_matching(self):
        res = self.client.get(MANUFACTURER_FORMAT_URL, data={"name": "Toyota"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Mitsubishi")

    def test_pagination(self):
        for i in range(8):
            Manufacturer.objects.create(name=f"m{i}", country="test_country")
        res = self.client.get(MANUFACTURER_FORMAT_URL)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.context.get("is_paginated"))
        objects = res.context["manufacturer_list"]
        self.assertEqual(len(objects), 5)
