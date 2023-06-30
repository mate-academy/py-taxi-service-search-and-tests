from django.urls import reverse

from tests.test_setup import TestSetUp


class PrivateTest(TestSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.driver)

    def test_search_manufacturers(self):
        url = (
            reverse("taxi:manufacturer-list")
            + "?name="
            + self.manufacturer_data["name"][2:]
        )
        response = self.client.get(url)
        manufacturers = [
            i
            for i in self.manufacturers
            if i.name[2:] == self.manufacturer_data["name"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            manufacturers
        )

    def test_search_drivers(self):
        url = (
            reverse("taxi:driver-list")
            + "?username="
            + self.driver_data["username"][2:]
        )
        response = self.client.get(url)
        drivers = [
            i
            for i in self.drivers
            if i.username[2:] == self.driver_data["username"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), drivers)

    def test_search_cars(self):
        url = reverse("taxi:car-list") + "?model=" + self.car_data["model"][2:]
        response = self.client.get(url)
        cars = [
            i for i in self.cars
            if i.model[2:] == self.car_data["model"][2:]
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), cars)
