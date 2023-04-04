from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


class DriverCreationFormTest(TestCase):
    def test_driver_creation_with_license_is_valid(self):
        form_data = {
            "username": "tester",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_license_number(self):

        invalid_license_numbers = [
            "AB12345",
            "ABC1234",
            "12345678",
            "abc12345",
            "ABC1234X",
            "ABC1234+",
            "A1234B56",
            "ABCD1234",
            "ABC12345X",
        ]

        for invalid_license_number in invalid_license_numbers:
            form_data = {"license_number": invalid_license_number}
            form = DriverLicenseUpdateForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn("license_number", form.errors)


class SearchFeatureTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="search_tester",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_driver_search_feature(self):
        name_query = "search_tester"
        response = self.client.get(
            reverse("taxi:driver-list"),
            data={"name": name_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(username__icontains=name_query),
        )

    def test_car_search_feature(self):
        manufacturer = Manufacturer.objects.create(
            name="Nissan",
            country="Japan"
        )
        Car.objects.create(model="Jiguli", manufacturer=manufacturer)
        Car.objects.create(model="Nivy", manufacturer=manufacturer)
        model_query = "Nivy"

        response = self.client.get(
            reverse("taxi:car-list"),
            data={"model": model_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains=model_query),
        )

    def test_manufacturer_search_feature(self):
        Manufacturer.objects.create(name="Nissan", country="Japan")
        name_query = "Ni"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            data={"name": name_query}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains=name_query),
        )
