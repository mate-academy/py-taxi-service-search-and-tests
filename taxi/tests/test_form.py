from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Manufacturer


class FormsCreationTests(TestCase):
    def test_driver_creation_form_with_additional_options(self):
        form_data = {
            "username": "user.name",
            "password1": "pass1user",
            "password2": "pass1user",
            "first_name": "Name",
            "last_name": "SurName",
            "license_number": "AAA11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_update_form_with_additional_options(self):
        form_data = {
            "license_number": "AAA11111"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class SearchFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test1_user",
            password="<PASSWORD>",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)

    def test_driver_search_by_username(self) -> None:
        get_user_model().objects.create_user(
            username="test_user", password="<PASSWORD>"
        )
        res = self.client.get(
            reverse("taxi:driver-list"), {"username": self.user.username}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.username)

    def test_car_search_by_model(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test manufacturer",
            country="Uk"
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        res = self.client.get(
            reverse("taxi:car-list"),
            {"model" : "test_model"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "test_model")

    def test_manufacturer_search_by_name(self) -> None:
        Manufacturer.objects.create(name="test manufacturer", country="Uk")
        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "test_manufacturer"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "test_manufacturer")
