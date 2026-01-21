from django.contrib.auth import get_user_model
from django.test import TestCase
from pyexpat import model

from taxi.forms import (DriverLicenseUpdateForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)
from taxi.models import Manufacturer, Car, Driver
from taxi.tests.tests_views import (CAR_LIST_URL,
                                    MANUFACTURER_LIST_URL,
                                    DRIVER_LIST_URL)


class FormsTests(TestCase):
    def test_driver_licence_valid(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_licence_invalid(self):
        form_data = {
            "license_number": "ABC1234"
        }
        form = DriverLicenseUpdateForm(form_data)
        self.assertTrue(not form.is_valid())
        self.assertEqual(form.cleaned_data, {})


class SearchTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_search_cars_by_model(self):
        form_data = {"model": "test_model"}

        form = CarSearchForm(form_data)
        self.assertTrue(form.is_valid())

        manufacturer = Manufacturer.objects.create(name="Test Manufacturer")
        Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model",
        )
        Car.objects.create(
            manufacturer=manufacturer,
            model="Test Model 2",
        )
        Car.objects.create(
            manufacturer=manufacturer,
            model="Random model",
        )
        res = self.client.get(CAR_LIST_URL, {"model": "Test", "page": 1})
        self.assertEqual(res.status_code, 200)
        cars = Car.objects.filter(model__icontains="Test")
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_manufacturer_search_by_name(self):
        form_data = {"name": "test_manufacturer"}

        form = ManufacturerSearchForm(form_data)
        self.assertTrue(form.is_valid())

        Manufacturer.objects.create(name="Test Manufacturer")
        Manufacturer.objects.create(name="Test Another Manufacturer")
        Manufacturer.objects.create(name="Random name")
        res = self.client.get(MANUFACTURER_LIST_URL, {
            "name": "Test", "page": 1
        })
        self.assertEqual(res.status_code, 200)
        manufacturers = Manufacturer.objects.filter(name__icontains="Test")
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_driver_search_by_username(self):
        form_data = {"username": "test_driver"}

        form = DriverSearchForm(form_data)
        self.assertTrue(form.is_valid())

        Driver.objects.create(
            username="TestDriver",
            password="<PASSWORD>",
            license_number="ABC12345",
        )
        Driver.objects.create(
            username="TestDriver1",
            password="<PASSWORD>",
            license_number="BBC12345",
        )
        Driver.objects.create(
            username="Random username",
            password="<PASSWORD>",
            license_number="CBC12345",
        )
        res = self.client.get(DRIVER_LIST_URL, {"username": "Test", "page": 1})
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.filter(username__icontains="Test")
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
