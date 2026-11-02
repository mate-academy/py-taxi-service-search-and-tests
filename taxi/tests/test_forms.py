from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer


class FormTests(TestCase):
    def setUp(self):
        self.data = {
            "username": "new_user",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "first_name": "Test",
            "last_name": "Driver",
            "license_number": "TST12345",
        }
        self.driver = get_user_model().objects.create_user(
            username="existing",
            license_number="AAA00001",
        )

    def test_creation_form_saves_custom_fields(self):
        form = DriverCreationForm(data=self.data)
        self.assertTrue(form.is_valid(), form.errors)
        driver = form.save()
        for field in ("username", "first_name", "last_name", "license_number"):
            self.assertEqual(getattr(driver, field), self.data[field])
        self.assertTrue(driver.check_password(self.data["password1"]))

    def test_license_update_preserves_other_fields(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "NEW54321"}, instance=self.driver
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "NEW54321")
        self.assertEqual(self.driver.username, "existing")

    def test_invalid_licenses_in_both_forms(self):
        invalid_numbers = (
            "AB12345", "ABCD12345", "abc12345", "AB112345", "ABC12X45"
        )

        for number in invalid_numbers:
            for form_class in (DriverCreationForm, DriverLicenseUpdateForm):
                with self.subTest(number=number, form=form_class.__name__):
                    form = form_class(
                        data={**self.data, "license_number": number}
                    )
                    self.assertFalse(form.is_valid())
                    self.assertIn("license_number", form.errors)

    def test_duplicate_license_in_both_forms(self):
        for form_class in (DriverCreationForm, DriverLicenseUpdateForm):
            with self.subTest(form=form_class.__name__):
                form = form_class(
                    data={**self.data, "license_number": "AAA00001"}
                )
                self.assertFalse(form.is_valid())
                self.assertIn("license_number", form.errors)

    def test_car_form_saves_selected_drivers(self):
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        form = CarForm(data={
            "model": "A4",
            "manufacturer": manufacturer.pk,
            "drivers": [self.driver.pk],
        })
        self.assertTrue(form.is_valid(), form.errors)
        car = form.save()
        self.assertEqual(car.manufacturer, manufacturer)
        self.assertEqual(list(car.drivers.all()), [self.driver])

    def test_search_forms(self):
        cases = (
            (DriverSearchForm, "username"),
            (CarSearchForm, "model"),
            (ManufacturerSearchForm, "name"),
        )

        for form_class, field in cases:
            for query, expected in (("", ""), ("  test  ", "test")):
                with self.subTest(form=form_class.__name__, query=query):
                    form = form_class(data={field: query})
                    self.assertTrue(form.is_valid(), form.errors)
                    self.assertEqual(form.cleaned_data[field], expected)

            with self.subTest(form=form_class.__name__, query="too long"):
                form = form_class(data={field: "a" * 256})
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)
