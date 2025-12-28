from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpass123", license_number="LIC00001"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpass123", license_number="LIC00002"
        )

    def test_driver_field_queryset(self):
        form = CarForm()
        self.assertEqual(len(form.fields["drivers"].queryset), 2)

    def test_form_save(self):
        form_data = {
            "model": "Model S",
            "manufacturer": Manufacturer.objects.create(name="Tesla"),
            "drivers": [self.user1.pk, self.user2.pk],
        }
        form = CarForm(data=form_data)
        if form.is_valid():
            car = form.save()
            self.assertEqual(car.drivers.count(), 2)
        else:
            self.fail(form.errors)


class DriverCreationFormTest(TestCase):
    def test_license_number_validation(self):
        form_data = {
            "username": "newdriver",
            "password1": "django1234",
            "password2": "django1234",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data["license_number"] = "abc12345"
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTest(TestCase):
    def test_license_number_clean_method(self):
        form_data = {"license_number": "XYZ67890"}
        form = DriverLicenseUpdateForm(data=form_data)
        if form.is_valid():
            self.assertEqual(form.cleaned_data["license_number"], "XYZ67890")
        else:
            self.fail(
                "Form should be valid with "
                "uppercase and digits in license number."
            )

        form_data["license_number"] = "xyz12345"
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
