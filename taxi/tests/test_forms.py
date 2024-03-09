from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class FormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(name="Subaru test")
        self.car = Car.objects.create(
            model="Boxer",
            manufacturer=self.manufacturer
        )

        self.driver = get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Boxer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boxer")
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Subaru"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subaru")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_driver_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver_test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_test")
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_license_number(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"license_number": "1234"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1234")
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_car_form_invalid(self):
        form_data = {
            "model": "TestModel",
            "manufacturers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_creation_form_invalid(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "invalid_license_number",
            "first_name": "John",
            "last_name": "Doe",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        form_data = {
            "license_number": "invalid_license_number",
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
