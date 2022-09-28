from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class PublicTestIndexView(TestCase):
    def test_login_required(self):
        response = self.client.get("")
        self.assertNotEqual(response.status_code, 200)


class PrivateTestIndexView(TestCase):
    def setUp(self) -> None:
        self.user_test = Driver.objects.create(
            username="test_username", password="test_password"
        )
        self.client.force_login(self.user_test)

    def test_login_required(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_num_visits(self):
        num_visits = 14
        for _ in range(num_visits):
            self.client.get("")
        response = self.client.get("")
        self.assertEqual(response.context["num_visits"], num_visits + 1)


class TestCarView(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_of_car = 22
        manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_country"
        )
        for i in range(num_of_car):
            Car.objects.create(model=f"test_model {i}", manufacturer=manufacturer)

    def setUp(self) -> None:
        self.user_test = Driver.objects.create(
            username="test_username", password="test_password"
        )
        self.client.force_login(self.user_test)

    def test_car_pagination(self):
        response = self.client.get(reverse("taxi:car-list") + "?page=5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertEqual(response.context["is_paginated"], True)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_car_detail_view_assign_delete(self):
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 1}))
        self.assertTrue(self.user_test in Driver.objects.filter(cars__id=1))
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 1}))
        self.assertFalse(self.user_test in Driver.objects.filter(cars__id=1))
