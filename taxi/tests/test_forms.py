from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Nissan", country="Japan"
        )
        self.driver = get_user_model().objects.create_user(
            username="driver1", password="test123", license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2", password="test321", license_number="DRV12345"
        )

        self.car1 = Car.objects.create(
            model="Skyline", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Civic", manufacturer=self.manufacturer
        )
        self.car1.drivers.set([self.driver])
        self.car2.drivers.set([self.driver2])

    def test_car_form_valid_data(self):
        form_data = {
            "model": "Skyline",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_with_all_data_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "TST12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_license_number_update(self):
        form_data = {"license_number": "TST12345"}
        form = DriverLicenseUpdateForm(data=form_data, instance=self.driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_search_form_validity(self):
        form = CarSearchForm(data={"model": "Skyline"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_functionality(self):
        response = self.client.get(reverse("car-list"), {"model": "Skyline"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)

        response = self.client.get(reverse("car-list"), {"model": "Civic"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car1.model)

    def test_empty_search_form(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Nissan"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_functionality(self):
        response = self.client.get(
            reverse("manufacturer-list"), {"name": "Nissan"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer.name)

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "driver1"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_functionality(self):
        response = self.client.get(
            reverse("driver-list"), {"username": "driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)
        self.assertNotContains(response, self.driver2.username)

    def test_no_results_found_in_search(self):
        response = self.client.get(
            reverse("car-list"), {"model": "NonexistentModel"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No results found")
