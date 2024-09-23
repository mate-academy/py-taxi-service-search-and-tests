from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from taxi.models import Car, Manufacturer


class CarViewTest(TestCase):
    def setUp(self):
        self.username = "usertest"
        self.password = "testpassword456"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="United Kingdom",
        )
        self.car = Car.objects.create(
            model="Test Car", manufacturer_id=self.manufacturer.id
        )
        self.client.force_login(self.user)

    def test_login_required_views(self):
        login_required_urls = [
            reverse_lazy("taxi:car-list"),
            reverse_lazy("taxi:car-create"),
            reverse_lazy("taxi:car-detail", args=[1]),
            reverse_lazy("taxi:car-update", args=[1]),
            reverse_lazy("taxi:car-delete", args=[1]),
        ]

        for url in login_required_urls:
            self.client.logout()
            response = self.client.get(url)
            expected_url = f"/accounts/login/?next={url}"

            self.assertNotEqual(response.status_code, 200)
            self.assertRedirects(response, expected_url)

            self.client.force_login(self.user)
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)

    def create_cars(self, instance_count):
        for car_id in range(1, instance_count + 1):
            manufacturer = Manufacturer.objects.create(
                name=f"name {car_id}",
                country=f"country {car_id}",
            )
            Car.objects.create(
                model=f"model {car_id}", manufacturer=manufacturer
            )

    def test_car_list_view_pagination(self):
        self.create_cars(10)
        response = self.client.get(reverse_lazy("taxi:car-list"))

        self.assertTrue(response.context["is_paginated"])
        self.assertTrue(len(response.context["car_list"]) == 5)

    def test_car_list_view_search(self):
        self.create_cars(10)
        response = self.client.get(
            reverse_lazy("taxi:car-list"), {"search": "Test Car"}
        )

        self.assertContains(response, self.car.model)
        self.assertTrue(len(response.context["car_list"]) == 1)

        response = self.client.get(
            reverse_lazy("taxi:car-list"), {"search": "model"}
        )

        self.assertTrue(len(response.context["car_list"]) == 5)

    def test_car_list_view_not_result_search(self):
        self.create_cars(10)
        response = self.client.get(
            reverse_lazy("taxi:car-list"), {"search": "qwerty"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["car_list"])

    def test_car_list_view_empty_search(self):
        self.create_cars(10)
        response = self.client.get(
            reverse_lazy("taxi:car-list"), {"search": ""}
        )

        self.assertTrue(len(response.context["car_list"]) == 5)

    def test_car_list_view_search_form_saves_get_parameters(self):
        response = self.client.get(
            reverse_lazy("taxi:car-list"),
            {"search": "Test Ca", "color": "blue"}
        )
        self.assertContains(
            response, '<input type="hidden" name="color" value="blue">'
        )
        self.assertNotContains(
            response,
            '<input type="hidden" name="search"'
        )

    def test_car_detail_view(self):
        response = self.client.get(
            reverse_lazy("taxi:car-detail", args=[self.car.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_car_delete_view(self):
        response = self.client.get(
            reverse_lazy("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse_lazy("taxi:car-delete", args=[self.car.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())

    def test_create_car_view(self):
        form_data = {
            "model": "model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }
        self.assertFalse(Car.objects.filter(model=form_data["model"]).exists())

        response = self.client.post(
            reverse_lazy("taxi:car-create"), data=form_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model=form_data["model"]).exists())

    def test_update_car_view(self):
        form_data = {
            "model": "model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user.pk],
        }

        self.assertFalse(Car.objects.filter(model=form_data["model"]).exists())

        response = self.client.post(
            reverse_lazy("taxi:car-update", args=[self.car.pk]), data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model=form_data["model"]).exists())
