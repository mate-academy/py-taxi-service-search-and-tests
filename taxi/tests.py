from django.test import TestCase
from django.contrib.auth import get_user_model


from django.urls import reverse
from taxi.forms import (
    CarModelSearchForm,
    DriverUsernameSearchForm,
    ManufacturerNameSearchForm,
)

HOME_PAGE = reverse("taxi:index")
DRIVERS_LIST = reverse("taxi:driver-list")
CARS_LIST = reverse("taxi:car-list")
MANUFACTURERS_LIST = reverse("taxi:manufacturer-list")


class TestsForPublicRequired(TestCase):

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list(self):
        response = self.client.get(DRIVERS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list(self):
        response = self.client.get(CARS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list(self):
        response = self.client.get(MANUFACTURERS_LIST)
        self.assertNotEqual(response.status_code, 200)


class TestsForPrivateRequired(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="dissom1987"
        )
        self.client.force_login(self.driver)

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertEqual(response.status_code, 200)

    def test_driver_list(self):
        response = self.client.get(DRIVERS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_car_list(self):
        response = self.client.get(CARS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list(self):
        response = self.client.get(MANUFACTURERS_LIST)
        self.assertEqual(response.status_code, 200)


class CarSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = CarModelSearchForm(data={"model": "Tesla model 3"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = CarModelSearchForm()
        self.assertFalse(form.is_valid())


class DriverSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = DriverUsernameSearchForm(data={"username": "DriverTest"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = DriverUsernameSearchForm()
        self.assertFalse(form.is_valid())


class ManufacturerSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = ManufacturerNameSearchForm(data={"name": "Tesla"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = ManufacturerNameSearchForm()
        self.assertFalse(form.is_valid())
