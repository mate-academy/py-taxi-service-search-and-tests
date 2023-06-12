from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "test123test",
            "password2": "test123test",
            "first_name": "Test",
            "last_name": "Test",
            "license_number": "AAA11111"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        request = "TEST"
        response = self.client.get(f"/manufacturers/?name={request}")
        queryset = response.context["manufacturer_list"]
        expected_queryset = Manufacturer.objects.filter(
            name__icontains=request
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_driver_search(self):
        request = "test.name"
        response = self.client.get(f"/drivers/?username={request}")
        queryset = response.context["driver_list"]
        expected_queryset = get_user_model().objects.filter(
            username__icontains=request
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(queryset), list(expected_queryset))

    def test_car_search(self):
        request = "TEST"
        response = self.client.get(f"/cars/?name={request}")
        queryset = response.context["car_list"]
        expected_queryset = Car.objects.filter(
            model__icontains=request
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(queryset), list(expected_queryset))
