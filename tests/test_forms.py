from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, SearchForm
from taxi.models import Car, Manufacturer
from tests.test_views import DRIVERS_LIST, CARS_LIST, MANUFACTURER_LIST


class CreateFormsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="TeJus2pwd",
            last_name="test_last_name",
            first_name="test_first_name"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test-country"
        )
        self.car = Car.objects.create(
            model="test_car",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.user)

        self.client.force_login(user=self.user)

    def test_form_create_car(self):
        car_data = {
            "model": "test model",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        self.client.post(reverse("taxi:car-create"), data=car_data)
        car = Car.objects.get(model=car_data["model"])
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(car.model, car_data["model"])
        self.assertTrue(self.user in car.drivers.all())

    def test_form_create_driver(self) -> None:
        driver_data = {
            "username": "testuser",
            "password1": "MNBJD*@2",
            "password2": "MNBJD*@2",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "license_number": "FIR12534"
        }
        self.client.post(reverse("taxi:driver-create"), data=driver_data)
        new_driver = get_user_model().objects.get(
            username=driver_data["username"]
        )

        self.assertEqual(new_driver.username, driver_data["username"])
        self.assertEqual(new_driver.first_name, driver_data["first_name"])
        self.assertEqual(new_driver.last_name, driver_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            driver_data["license_number"]
        )

    def test_check_user_creation_form_with_valid_data(self):
        user_data = {
            "username": "test_user2",
            "password1": "smthp2swd",
            "password2": "smthp2swd",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }
        form = DriverCreationForm(data=user_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, user_data)

    def test_search_form_for_driver_by_username(self):
        search_data = {"username": self.user.username}
        form = SearchForm(data=search_data)
        response = self.client.get(DRIVERS_LIST, data=search_data)
        self.assertTrue(form.is_valid())
        self.assertContains(response, self.user.username)
        self.assertEqual(response.status_code, 200)

    def test_search_form_for_car_by_model(self):
        search_data = {"model": self.car.model}
        form = SearchForm(data=search_data)
        response = self.client.get(CARS_LIST, data=search_data)
        self.assertTrue(form.is_valid())
        self.assertContains(response, self.car.model)
        self.assertEqual(response.status_code, 200)

    def test_search_form_for_manufacturer_by_name(self):
        search_data = {"name": self.manufacturer.name}
        form = SearchForm(data=search_data)
        response = self.client.get(MANUFACTURER_LIST, data=search_data)
        self.assertTrue(form.is_valid())
        self.assertContains(response, self.manufacturer.name)
        self.assertEqual(response.status_code, 200)
