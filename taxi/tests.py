from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm


HOME_PAGE = reverse("taxi:index")
DRIVERS_LIST = reverse("taxi:driver-list")
CARS_LIST = reverse("taxi:car-list")
MANUFACTURERS_LIST = reverse("taxi:manufacturer-list")


class CarSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = CarSearchForm(data={"model": "Test Car"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = CarSearchForm()
        self.assertFalse(form.is_valid())


class DriverSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = DriverSearchForm(data={"username": "TestUser"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = DriverSearchForm()
        self.assertFalse(form.is_valid())


class ManufacturerSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = ManufacturerSearchForm(data={"name": "TestManufacturer"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = ManufacturerSearchForm()
        self.assertFalse(form.is_valid())


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
            username="test.user",
            password="test123"
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
