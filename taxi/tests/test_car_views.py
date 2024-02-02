from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi import forms
from taxi.models import Car, Driver, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test_driver",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

        number_of_cars = 12

        for car_id in range(number_of_cars):
            car = Car.objects.create(
                model=f"Car {car_id}",
                manufacturer=Manufacturer.objects.create(
                    name=f"Manufacturer {car_id}", country=f"Country: {car_id}"
                ),
            )
            car.drivers.set(
                [
                    Driver.objects.create(
                        username=f"Driver {car_id}",
                        password=f"test12{car_id}",
                        license_number=f"plate25{car_id}",
                    )
                ]
            )

    def test_view_url_exists(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_view_have_search_form_context(self):
        response = self.client.get(CAR_URL)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], forms.CarSearchForm
        )

    def test_existing_pagination(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["cars_list"]), 5)

    def test_pagination_paged(self):
        response = self.client.get(CAR_URL + "?page=3")
        self.assertEqual(len(response.context["cars_list"]), 2)

    def test_correct_query_set(self):
        response = self.client.get(CAR_URL, {"model": "Car 3"})
        self.assertContains(response, "Car 3")
        self.assertNotContains(response, "Car 4")

    def test_car_detail_view_exist(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[Car.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_assigning_in_car_detail_view_exist(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[Car.objects.first().pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_update_car_view_exist(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[Car.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_car_view_exist(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[Car.objects.first().pk])
        )
        self.assertEqual(response.status_code, 200)
