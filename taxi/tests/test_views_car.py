from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarForm
from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


# CAR_CREATE_URL = reverse("taxi:cars-create")


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200, )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/cars/")


class PrivateCarListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        number_of_cars = 8
        for car_num in range(number_of_cars):
            Car.objects.create(
                model=f"X5 {car_num}",
                manufacturer=manufacturer
            )

    def test_car_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/cars/")
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_url_accessible_by_name(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_uses_correct_template(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_pagination_is_five(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["car_list"]) == 5)

    def test_car_lists_all_cars(self):
        response = self.client.get(CAR_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["car_list"]) == 3)


class PrivateCarCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.form_data = {
            "model": "X5",
            "manufacturer": manufacturer.id,
            "drivers": [],
        }

    def test_create_car(self):
        self.client.post(reverse("taxi:car-create"), data=self.form_data)
        # new_car = Car.objects.get(model=self.form_data["model"])
        # self.assertEqual(new_car.model, self.form_data["model"])
