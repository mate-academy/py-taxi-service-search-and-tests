from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test", password="12345"
        )
        self.client.login(username="Test", password="12345")

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car = Car.objects.create(
            model="x5",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

    def test_manufacturer_search_form(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "bmw"}
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name, "BMW"
        )

    def test_driver_search_form(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Test"}
        )
        self.assertTrue(
            any(driver.username == "Test"
                for driver in response.context["driver_list"])
        )

    def test_car_search_form(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model_": "x5"}
        )
        self.assertTrue(
            any(car.model == "x5"
                for car in response.context["car_list"])
        )

    def test_car_search_form_no_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model_": "x6"}
        )
        self.assertFalse(
            any(car.model == "x6"
                for car in response.context["car_list"])
        )

    def test_car_search_form_empty(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model_": ""}
        )
        self.assertEqual(
            response.context["car_list"].count(), Car.objects.count()
        )

    def test_car_search_form_no_results_empty(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model_": "x6"}
        )
        self.assertFalse(
            any(car.model == "x6"
                for car in response.context["car_list"])
        )

    def test_view_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.context["car"], self.car)

    def test_view_car_detail_no_results(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_model_search_form(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "bmw"}
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name, "BMW"
        )

    def test_model_search_form_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "bmw"}
        )
        self.assertEqual(
            response.context["manufacturer_list"][0].name, "BMW"
        )

    def test_forms(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Test"}
        )
        self.assertTrue(
            any(driver.username == "Test"
                for driver in response.context["driver_list"])
        )

    def test_forms_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "Test"}
        )
        self.assertTrue(
            any(driver.username == "Test"
                for driver in response.context["driver_list"])
        )
