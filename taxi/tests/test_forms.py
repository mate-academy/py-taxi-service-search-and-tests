from django import forms
from django.test import TestCase

from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


class DriverCreationFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "jim.hopper",
            "first_name": "Jim",
            "last_name": "Hopper",
            "license_number": "ABC12345",
            "password1": "R8!vQ2#nZ5@kL9",
            "password2": "R8!vQ2#nZ5@kL9",
        }

    def test_form_accepts_valid_license_number(self):
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data["license_number"],
            "ABC12345",
        )

    def test_form_saves_additional_fields(self):
        form = DriverCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid(), form.errors)

        driver = form.save()
        driver.refresh_from_db()

        self.assertEqual(driver.username, "jim.hopper")
        self.assertEqual(driver.first_name, "Jim")
        self.assertEqual(driver.last_name, "Hopper")
        self.assertEqual(driver.license_number, "ABC12345")

    def test_license_number_too_short(self):
        self.form_data["license_number"] = "ABC1234"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_too_long(self):
        self.form_data["license_number"] = "ABC123456"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_starts_with_lowercase_letters(self):
        self.form_data["license_number"] = "abc12345"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_starts_with_mixed_case_letters(self):
        self.form_data["license_number"] = "AbC12345"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_digit_in_prefix(self):
        self.form_data["license_number"] = "AB112345"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_symbol_in_prefix(self):
        self.form_data["license_number"] = "AB!12345"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_letter_in_suffix(self):
        self.form_data["license_number"] = "ABC1234D"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_symbol_in_suffix(self):
        self.form_data["license_number"] = "ABC1234!"

        form = DriverCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class DriverLicenseUpdateFormTests(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="jim.hopper",
            first_name="Jim",
            last_name="Hopper",
            license_number="ABC12345",
        )

    def test_form_updates_license_number(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67890"},
            instance=self.driver,
        )

        self.assertTrue(form.is_valid(), form.errors)

        form.save()
        self.driver.refresh_from_db()

        self.assertEqual(self.driver.license_number, "DEF67890")
        self.assertEqual(self.driver.username, "jim.hopper")
        self.assertEqual(self.driver.first_name, "Jim")
        self.assertEqual(self.driver.last_name, "Hopper")
        self.assertEqual(Driver.objects.count(), 1)

    def test_form_exposes_only_license_number(self):
        form = DriverLicenseUpdateForm(instance=self.driver)

        self.assertEqual(
            list(form.fields),
            ["license_number"],
        )

    def test_license_number_too_short(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_too_long(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC123456"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_starts_with_lowercase_letters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_starts_with_mixed_case_letters(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "AbC12345"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_digit_in_prefix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "AB112345"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_symbol_in_prefix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "AB!12345"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_letter_in_suffix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234D"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_contains_symbol_in_suffix(self):
        form = DriverLicenseUpdateForm(
            data={"license_number": "ABC1234!"},
            instance=self.driver,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        self.jim = Driver.objects.create_user(
            username="jim.hopper",
            license_number="ABC12345",
        )
        self.anna = Driver.objects.create_user(
            username="anna",
            license_number="DEF67890",
        )
        self.other_driver = Driver.objects.create_user(
            username="other_driver",
            license_number="GHI54321",
        )

    def test_drivers_field_uses_checkboxes(self):
        form = CarForm()

        self.assertIsInstance(
            form.fields["drivers"].widget,
            forms.CheckboxSelectMultiple,
        )

    def test_drivers_field_includes_available_drivers(self):
        form = CarForm()

        self.assertCountEqual(
            form.fields["drivers"].queryset,
            [self.jim, self.anna, self.other_driver],
        )

    def test_form_saves_selected_drivers(self):
        form = CarForm(
            data={
                "model": "X5",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.jim.pk, self.anna.pk],
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

        car = form.save()
        car.refresh_from_db()

        self.assertEqual(car.model, "X5")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertCountEqual(
            car.drivers.all(),
            [self.jim, self.anna],
        )

    def test_form_updates_selected_drivers(self):
        car = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.jim, self.anna)

        form = CarForm(
            data={
                "model": "X5",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.anna.pk, self.other_driver.pk],
            },
            instance=car,
        )

        self.assertTrue(form.is_valid(), form.errors)

        form.save()
        car.refresh_from_db()

        self.assertCountEqual(
            car.drivers.all(),
            [self.anna, self.other_driver],
        )

    def test_form_requires_at_least_one_driver(self):
        form = CarForm(
            data={
                "model": "X5",
                "manufacturer": self.manufacturer.pk,
                "drivers": [],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)
