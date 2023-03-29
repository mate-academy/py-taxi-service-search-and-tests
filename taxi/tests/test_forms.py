from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Car, Manufacturer


class DataFormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password",
            "password2": "test_password",
            "license_number": "LLL98764",
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test_password"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        search_request = "test_search"
        response = self.client.get(f"/drivers/?username={search_request}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(username__icontains=search_request)
        )

    def test_car_search(self):
        search_request = "test_search"
        response = self.client.get(f"/cars/?model={search_request}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains=search_request)
        )

    def test_manufacturer_search(self):
        search_request = "test_search"
        response = self.client.get(f"/manufacturers/?name={search_request}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains=search_request)
        )
