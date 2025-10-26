from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PrivateSearchViewTestBase(TestCase):
    def setUp(self) -> None:

        self.user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.user)

        self.m1 = Manufacturer.objects.create(name="Audi", country="DE")
        self.m2 = Manufacturer.objects.create(name="BMW", country="DE")
        self.m3 = Manufacturer.objects.create(name="Mercedes", country="DE")

        self.car1 = Car.objects.create(model="A4", manufacturer=self.m1)
        self.car2 = Car.objects.create(model="Q7", manufacturer=self.m1)
        self.car3 = Car.objects.create(model="X3", manufacturer=self.m2)

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="123",
            license_number="AAA111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="123",
            license_number="BBB222"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="john_doe",
            password="123",
            license_number="CCC333"
        )


class ManufacturerSearchViewTest(PrivateSearchViewTestBase):

    def test_search_manufacturer_found(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "B"})
        self.assertEqual(response.status_code, 200)

        manufacturers = response.context["manufacturer_list"]
        self.assertIn(self.m2, manufacturers)  # BMW
        self.assertNotIn(self.m1, manufacturers)
        self.assertNotIn(self.m3, manufacturers)

    def test_search_manufacturer_no_results(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": "ZZZ"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            list(response.context["manufacturer_list"]), []
        )

    def test_search_manufacturer_empty_query(self):
        response = self.client.get(MANUFACTURER_LIST_URL, {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            list(response.context["manufacturer_list"]),
            [self.m1, self.m2, self.m3],
            ordered=False
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarSearchViewTest(PrivateSearchViewTestBase):
    def test_search_car_found(self):
        response = self.client.get(CAR_LIST_URL, {"model": "A"})
        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)
        self.assertNotIn(self.car3, cars)

    def test_search_car_no_results(self):
        response = self.client.get(CAR_LIST_URL, {"model": "ZZZ"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(list(response.context["car_list"]), [])

    def test_search_car_empty_query(self):
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            list(response.context["car_list"]),
            [self.car1, self.car2, self.car3],
            ordered=False
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverSearchViewTest(PrivateSearchViewTestBase):

    def test_search_driver_found(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "driver"})
        self.assertEqual(response.status_code, 200)

        drivers = response.context["driver_list"]
        self.assertIn(self.driver1, drivers)
        self.assertIn(self.driver2, drivers)
        self.assertNotIn(self.driver3, drivers)

    def test_search_driver_no_results(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "ZZZ"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(list(response.context["driver_list"]), [])

    def test_search_driver_empty_query(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            list(response.context["driver_list"]),
            [self.driver1, self.driver2, self.driver3],
            ordered=False
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
