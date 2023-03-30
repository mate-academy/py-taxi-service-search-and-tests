from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ASD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search_form(self):
        search_request = "BMW"
        response = self.client.get(f"/manufacturers/?name={search_request}")
        result_queryset = response.context["manufacturer_list"]
        expected_queryset = Manufacturer.objects.filter(
            name__icontains=search_request
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(result_queryset), list(expected_queryset))

    def test_driver_search_form(self):
        search_request = "john.smith"
        response = self.client.get(f"/drivers/?username={search_request}")
        result_queryset = response.context["driver_list"]
        expected_queryset = get_user_model().objects.filter(
            username__icontains=search_request
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(result_queryset), list(expected_queryset))

    def test_car_search_form(self):
        search_request = "X5"
        response = self.client.get(f"/cars/?model={search_request}")
        result_queryset = response.context["car_list"]
        expected_queryset = Car.objects.filter(model__icontains=search_request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(result_queryset), list(expected_queryset))
