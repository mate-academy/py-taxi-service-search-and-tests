from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.tests.test_views.initial_data import DRIVERS_URLS


class DriverListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 8

        for driver_id in range(1, number_of_drivers + 1):
            get_user_model().objects.create_user(
                username=f"test_username_{driver_id}",
                license_number=f"test_license_{driver_id}",
                password=f"test{driver_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)

    def test_drivers_pagination_is_five(self):
        response = self.client.get(DRIVERS_URLS["test_driver_list_url"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_drivers(self):
        response = self.client.get(
            f"{DRIVERS_URLS['test_driver_list_url']}?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_driver_get_context_data(self):
        response = self.client.get(
            f"{DRIVERS_URLS['test_driver_list_url']}?username=test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["username"],
            "test"
        )

    def test_drivers_get_queryset(self):
        response = self.client.get(
            f"{DRIVERS_URLS['test_driver_list_url']}?username=test_username_1"
        )
        queryset = response.context_data["object_list"]
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.user)

    def test_drivers_search_pagination(self):
        response = self.client.get(
            f"{DRIVERS_URLS['test_driver_list_url']}?username=test&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_drivers_search_no_page(self):
        response = self.client.get(
            f"{DRIVERS_URLS['test_driver_list_url']}?username=nonexistent"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 0)


class DriverDetailTest(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="test")
        self.car1 = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.car2 = Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="test_license",
            password="test1234",
        )
        self.car1.drivers.add(self.user)
        self.car2.drivers.add(self.user)

        self.client.force_login(self.user)

    def test_view_returns_correct_driver_data(self):
        response = self.client.get(DRIVERS_URLS["test_driver_detail_url"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver"].username,
            "test_username"
        )
        self.assertEqual(
            response.context["driver"].license_number,
            "test_license"
        )

    def test_view_returns_correct_cars_data(self):
        response = self.client.get(DRIVERS_URLS["test_driver_detail_url"])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context["driver"].cars.values_list("id", flat=True)),
            [self.car1.id, self.car2.id]
        )
