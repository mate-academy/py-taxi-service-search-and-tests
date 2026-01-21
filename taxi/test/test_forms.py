from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class DriverSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="testpassword",
            first_name="Test",
            last_name="Test",
            license_number="ABC12345"
        )
        self.non_matching_driver = get_user_model().objects.create_user(
            username="random_driver",
            password="randompassword",
            first_name="Random",
            last_name="Random",
            license_number="XYZ67890"
        )

    def test_driver_search_form_valid_data(self) -> None:
        form_data = {"username": "test"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        drivers = get_user_model().objects.filter(
            username__icontains=form_data["username"]
        )
        self.assertIn(self.driver, drivers)
        self.assertNotIn(self.non_matching_driver, drivers)
        self.assertEqual(list(drivers), [self.driver])


class CarSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.car_1 = Car.objects.create(
            model="test_model_1",
            manufacturer=self.manufacturer
        )
        self.car_2 = Car.objects.create(
            model="test_model_2",
            manufacturer=self.manufacturer
        )
        self.non_matching_car = Car.objects.create(
            model="random_model",
            manufacturer=self.manufacturer
        )

    def test_car_search_form_valid_data(self) -> None:
        form_data = {"model": "test_model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        cars = Car.objects.filter(
            model__icontains=form_data["model"]
        )
        self.assertIn(self.car_1, cars)
        self.assertIn(self.car_2, cars)
        self.assertNotIn(self.non_matching_car, cars)
        self.assertEqual(list(cars), [self.car_1, self.car_2])


class ManufacturerSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        self.non_matching_manufacturer = Manufacturer.objects.create(
            name="random_manufacturer",
            country="test_country"
        )

    def test_manufacturer_search_form_valid_data(self) -> None:
        form_data = {"name": "test_manufacturer"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        manufacturers = Manufacturer.objects.filter(
            name__icontains=form_data["name"]
        )
        self.assertIn(self.manufacturer, manufacturers)
        self.assertNotIn(self.non_matching_manufacturer, manufacturers)
        self.assertEqual(list(manufacturers), [self.manufacturer])
