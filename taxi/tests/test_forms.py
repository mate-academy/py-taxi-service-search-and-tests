from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


class FormsTests(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "test_username",
            "password1": "test_password1234",
            "password2": "test_password1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "WWW12345",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form(self):
        form_data = {"license_number": "WWW54321"}

        form = DriverLicenseUpdateForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "MAO", "test_password1234"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        response = self.client.get("/drivers/?username=MAO")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="MAO")
        )

    def test_car_search(self):
        response = self.client.get("/cars/?model=audi")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="audi"),
        )

    def test_manufacturer_search(self):
        response = self.client.get("/manufacturers/?name=Audi")
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Audi")
        )
