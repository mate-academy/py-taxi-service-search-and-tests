from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car
from django.test import TestCase
from django.contrib.auth import get_user_model


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

    def test_driver_license_update_form_valid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "ABC12345",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_invalid(self):
        user = get_user_model().objects.create(username="test_user")
        form_data = {
            "license_number": "invalid_license",
        }
        form = DriverLicenseUpdateForm(instance=user, data=form_data)
        self.assertFalse(form.is_valid())


class FormSearchTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Subaru test")
        Car.objects.create(
            model="Boxer",
            manufacturer=manufacturer
        )
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Boxer"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boxer")
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Subaru test")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Subaru"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subaru")
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver_test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver_test")
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_license_number(self):
        get_user_model().objects.create_user(
            username="driver_test",
            password="12345driver",
            license_number="1234"
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"license_number": "1234"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1234")
        self.assertTemplateUsed(response, "taxi/driver_list.html")
