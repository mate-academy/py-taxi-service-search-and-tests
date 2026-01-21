from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

URL_DRIVER_LIST = "taxi:driver-list"
URL_CAR_LIST = "taxi:car-list"


class TestCarListSearchView(TestCase):
    def setUp(self):
        self.manufacturer = (
            Manufacturer.objects.create(name="Test Manufacturer")
        )

        Car.objects.create(model="Mercedes", manufacturer=self.manufacturer)
        Car.objects.create(model="Toyota", manufacturer=self.manufacturer)

    def test_car_list_search(self) -> None:
        response = self.client.get(reverse(URL_CAR_LIST) + "?model=BMW")

        if response.context:
            self.assertIn("car_list", response.context)
            car = Car.objects.filter(model="BMW")
            self.assertEqual(
                list(response.context["car_list"]),
                list(car)
            )

    def test_car_list_search_without_results(self) -> None:
        response = (
            self.client.get(reverse(URL_CAR_LIST) + "?model=Nonexistent Car")
        )

        if response.context:
            self.assertIn("car_list", response.context)
            self.assertFalse(response.context["car_list"])


class TestDriverListSearchView(TestCase):
    def setUp(self):
        Driver.objects.create(username="testdriver1", license_number="12345")
        Driver.objects.create(username="testdriver2", license_number="67890")

    def test_driver_list_search(self) -> None:
        response = (
            self.client.get(reverse(URL_DRIVER_LIST) + "?username=testdriver1")
        )

        if response.context:
            self.assertIn("driver_list", response.context)
            driver = Driver.objects.filter(username="testdriver1")
            self.assertEqual(
                list(response.context["driver_list"]),
                list(driver)
            )

    def test_driver_list_search_without_results(self) -> None:
        response = (
            self.client.get(reverse(URL_DRIVER_LIST) + "?username=none_driver")
        )

        if response.context:
            self.assertIn("driver_list", response.context)
            self.assertFalse(response.context["driver_list"])
