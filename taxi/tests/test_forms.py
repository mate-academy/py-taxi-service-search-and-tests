from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    DriverSearchForm,
    CarSearchForm
)


class FormsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)

    def test_driver_creation_with_license_number_first_last_name_is_valid(self):
        form_data = {
            "username": "user",
            "password1": "user11pass",
            "password2": "user11pass",
            "first_name": "first_name",
            "last_name": "last_name",
            "license_number": "AIO34333",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])
        self.assertEqual(form.cleaned_data["first_name"], form_data["first_name"])
        self.assertEqual(form.cleaned_data["last_name"], form_data["last_name"])
        self.assertEqual(form.cleaned_data["license_number"], form_data["license_number"])
        self.assertEqual(len(form.cleaned_data["license_number"]), 8)

    def test_driver_creation_form_contains_license_number_first_last_name_fields(self):
        url = reverse("taxi:driver-create")
        res = self.client.get(url)
        self.assertContains(res, "name=\"license_number\"")
        self.assertContains(res, "name=\"first_name\"")
        self.assertContains(res, "name=\"last_name\"")

    def test_license_update_form_changing_number(self):
        driver = get_user_model().objects.create_user(
            username="driver",
            password="testpass",
            license_number="AAA55555",
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "AIO34333"},
            instance=driver,
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "AIO34333")

    def test_manufacturer_search_form_with_empty_query_param(self):
        form = ManufacturerSearchForm(
            data={"name": ""}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
        self.assertTrue(form.fields["name"].label is None or form.fields["name"].label == "")

    def test_manufacturer_search_form_with_query_param(self):
        form = ManufacturerSearchForm(
            data={"name": "a"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "a")

    def test_driver_search_form_with_empty_query_param(self):
        form = DriverSearchForm(
            data={"username": ""}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")
        self.assertTrue(form.fields["username"].label is None or form.fields["username"].label == "")

    def test_driver_search_form_with_query_param(self):
        form = DriverSearchForm(
            data={"username": "h"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "h")

    def test_car_search_form_with_empty_query_param(self):
        form = CarSearchForm(
            data={"model": ""}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")
        self.assertTrue(form.fields["model"].label is None or form.fields["model"].label == "")

    def test_car_search_form_with_query_param(self):
        form = CarSearchForm(
            data={"model": "b"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "b")
