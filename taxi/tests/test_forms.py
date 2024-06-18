from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm

DRIVER = {
    "username": "test",
    "license_number": "RTG34567",
    "first_name": "test_first",
    "last_name": "test_last",
    "password1": "Struhanets87*",
    "password2": "Struhanets87*",
}


class TestForms(TestCase):
    def test_driver_creation_form_fields_is_valid(self):
        form = DriverCreationForm(data=DRIVER)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, DRIVER)


class PrivateDriverCreationFormTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="new_user",
            password="password123",
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        self.client.post(reverse("taxi:driver-create"), data=DRIVER)
        new_driver = get_user_model().objects.get(username=DRIVER["username"])

        self.assertEqual(new_driver.first_name, DRIVER["first_name"])
        self.assertEqual(new_driver.license_number, DRIVER["license_number"])
        self.assertEqual(new_driver.last_name, DRIVER["last_name"])


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="new_user",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_search_car(self):
        manufacturer = {
            "name": "test_manufacture",
            "country": "test_country",
        }
        car = {
            "model": "test_model",
            "manufacturer": manufacturer,
            "driver": DRIVER,
        }

        response = self.client.get(
            reverse("taxi:car-list"),
            data=car
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, car["model"])
