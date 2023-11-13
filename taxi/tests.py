from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm, DriverSearchForm
from taxi.models import Car, Manufacturer, Driver


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test", password="12345")
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

    def test_car_search_form(self):
        form = CarSearchForm(data={"model": "x5"})
        response = self.client.get(reverse("taxi:car-list"), {"model": "X5"})
        self.assertTrue(form.is_valid())
        self.assertEqual(response.context["car_list"][0].model, "x5")
        response = self.client.get(reverse(
            "taxi:car-list"), {"model": "noname"})
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_manufacturer_search_form(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "bmw"})
        self.assertEqual(response.context["manufacturer_list"][0].name, "BMW")

    def test_driver_search_form(self):
        response = self.client.get(reverse(
            "taxi:driver-list"), {"username": "Test"})
        self.assertTrue(any(driver.username == "Test"
                            for driver in response.context["driver_list"]))
