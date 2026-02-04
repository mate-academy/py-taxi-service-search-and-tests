from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.tests.test_driver_list_views import (
    TEST_DATA_1 as TEST_DRIVER_DATA
)
from taxi.tests.test_manufacturer_list_views import (
    TEST_DATA_1 as TEST_MANUFACTURER_DATA
)

from taxi.models import Manufacturer, Car, Driver

CARS_URL = reverse("taxi:car-list")
TEMPLATE_NAME = "taxi/car_list.html"
CONTEXT_OBJECT_NAME = "car_list"

TEST_DATA_1 = {
    "model": "test_model_1",
}
TEST_DATA_2 = {
    "model": "test_model_2",
}


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CARS_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        test_manufacturer = Manufacturer.objects.create(
            **TEST_MANUFACTURER_DATA
        )
        TEST_DATA_1["manufacturer"] = test_manufacturer
        TEST_DATA_2["manufacturer"] = test_manufacturer
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        driver = Driver.objects.create(**TEST_DRIVER_DATA)
        car1 = Car.objects.create(**TEST_DATA_1)
        car1.drivers.add(driver)
        car2 = Car.objects.create(**TEST_DATA_2)
        car2.drivers.add(driver)
        res = self.client.get(CARS_URL)
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(res.context[CONTEXT_OBJECT_NAME]),
            list(cars)
        )
        self.assertTemplateUsed(
            res, TEMPLATE_NAME
        )

    def test_search_cars(self):
        driver = Driver.objects.create(**TEST_DRIVER_DATA)
        car1 = Car.objects.create(**TEST_DATA_1)
        car1.drivers.add(driver)
        car2 = Car.objects.create(**TEST_DATA_2)
        car2.drivers.add(driver)
        query = TEST_DATA_1["model"][-5:]

        res = self.client.get(
            CARS_URL, {"model": query}
        )
        self.assertEqual(
            res.context["search_form"].initial["model"], query
        )
        self.assertIn(car1, res.context[CONTEXT_OBJECT_NAME])
        self.assertNotIn(car2, res.context[CONTEXT_OBJECT_NAME])
