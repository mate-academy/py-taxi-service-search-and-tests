from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer
from taxi.forms import CarModelSearchForm, CarForm

CAR_URL = reverse("taxi:car-list")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        for car_id in range(8):
            Car.objects.create(
                model=f"test_model-{car_id}",
                manufacturer=manufacturer
            )

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="admin", password="testpass123"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturer(self) -> None:
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_second_page(self):
        response = self.client.get(CAR_URL + "?page=2")

        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEquals(len(response.context["car_list"]), 3)

    def test_car_list_view_with_search(self):
        search_param = "?model=test_model-1"
        response = self.client.get(CAR_URL + search_param)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_model-1")
        self.assertNotContains(response, "test_model-2")
