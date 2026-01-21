from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car
from taxi.tests.test_views.initial_data import CAR_URLS


class CarListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        number_of_cars = 8

        for car_id in range(1, number_of_cars + 1):
            car = Car.objects.create(
                model=f"test_model_{car_id}",
                manufacturer=manufacturer,
            )
            car.drivers.add(user)

    def setUp(self):
        self.car = Car.objects.get(id=1)
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_cars_pagination_is_five(self):
        response = self.client.get(CAR_URLS["test_car_list_url"])
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_lists_all_cars(self):
        response = self.client.get(
            f"{CAR_URLS['test_car_list_url']}?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_car_get_context_data(self):
        response = self.client.get(
            f"{CAR_URLS['test_car_list_url']}?model=test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context_data)
        self.assertEqual(
            response.context_data["search_form"].initial["model"],
            "test"
        )

    def test_car_get_queryset(self):
        response = self.client.get(
            f"{CAR_URLS['test_car_list_url']}?model=test_model_1"
        )
        queryset = response.context_data["object_list"]
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0], self.car)

    def test_cars_search_pagination(self):
        response = self.client.get(
            f"{CAR_URLS['test_car_list_url']}?model=test&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_cars_search_no_page(self):
        response = self.client.get(
            f"{CAR_URLS['test_car_list_url']}?model=nonexistent"
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 0)


class CarDetailTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country",
        )

        self.user1 = get_user_model().objects.create_user(
            username="test_username1",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.user2 = get_user_model().objects.create_user(
            username="test_username2",
            license_number="ABC12347",
            password="Test1234q",
        )

        self.car = Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )

        self.car.drivers.add(self.user1)
        self.car.drivers.add(self.user2)

        self.client.force_login(self.user1)

    def test_view_returns_correct_car_data(self):
        response = self.client.get(CAR_URLS["test_car_detail_url"])
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["car"].model,
            "test_model"
        )
        self.assertEqual(
            response.context["car"].manufacturer,
            self.manufacturer
        )

    def test_view_returns_correct_drivers_data(self):
        response = self.client.get(CAR_URLS["test_car_detail_url"])
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            list(response.context["car"].drivers.values_list(
                "id", flat=True
            )),
            [self.user1.id, self.user2.id]
        )
