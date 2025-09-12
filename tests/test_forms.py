from django.test import TestCase
from django.contrib.auth import get_user_model
from django.forms.widgets import CheckboxSelectMultiple

from taxi.models import Manufacturer, Car

Driver = get_user_model()


class ManufacturerSearchFormTests(TestCase):
    def test_valid_when_empty(self):
        from taxi.forms import ManufacturerSearchForm
        form = ManufacturerSearchForm(data={"title": ""})
        self.assertTrue(form.is_valid())

    def test_valid_when_has_value(self):
        from taxi.forms import ManufacturerSearchForm
        form = ManufacturerSearchForm(data={"title": "toy"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "toy")

    def test_max_length_exceeded(self):
        from taxi.forms import ManufacturerSearchForm
        form = ManufacturerSearchForm(data={"title": "x" * 256})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_placeholder_and_label(self):
        from taxi.forms import ManufacturerSearchForm
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["title"].label, "")
        self.assertEqual(
            form.fields["title"].widget.attrs.get("placeholder"),
            "Search by name",
        )


class CarSearchFormTests(TestCase):
    def test_valid_when_empty(self):
        from taxi.forms import CarSearchForm
        form = CarSearchForm(data={"title": ""})
        self.assertTrue(form.is_valid())

    def test_placeholder_and_label(self):
        from taxi.forms import CarSearchForm
        form = CarSearchForm()
        self.assertEqual(form.fields["title"].label, "")
        self.assertEqual(
            form.fields["title"].widget.attrs.get("placeholder"),
            "Search by model",
        )


class DriverSearchFormTests(TestCase):
    def test_valid_when_empty(self):
        from taxi.forms import DriverSearchForm
        form = DriverSearchForm(data={"title": ""})
        self.assertTrue(form.is_valid())

    def test_placeholder_and_label(self):
        from taxi.forms import DriverSearchForm
        form = DriverSearchForm()
        self.assertEqual(form.fields["title"].label, "")
        self.assertEqual(
            form.fields["title"].widget.attrs.get("placeholder"),
            "Search by driver",
        )


class CarFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manuf = Manufacturer.objects.create(name="Toyota", country="Japan")
        cls.d1 = Driver.objects.create_user(
            username="john", password="x", license_number="ABC12345"
        )
        cls.d2 = Driver.objects.create_user(
            username="jane", password="x", license_number="DEF67890"
        )

    def test_widget_type_is_checkbox_select_multiple(self):
        from taxi.forms import CarForm
        form = CarForm()
        self.assertIsInstance(
            form.fields["drivers"].widget,
            CheckboxSelectMultiple
        )

    def test_create_car_with_drivers(self):
        from taxi.forms import CarForm
        data = {
            "model": "Supra",
            "manufacturer": str(self.manuf.id),
            "drivers": [str(self.d1.id), str(self.d2.id)],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
        car = form.save()
        self.assertEqual(car.model, "Supra")
        self.assertEqual(car.manufacturer, self.manuf)
        self.assertCountEqual(list(car.drivers.all()), [self.d1, self.d2])


class DriverCreationFormTests(TestCase):
    def test_creates_user_with_valid_license(self):
        from taxi.forms import DriverCreationForm
        form = DriverCreationForm(
            data={
                "username": "newuser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "license_number": "ABC12345",
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertIsInstance(user, Driver)
        self.assertEqual(user.license_number, "ABC12345")
        self.assertEqual(user.first_name, "John")
        self.assertTrue(user.check_password("StrongPass123"))

    def test_license_length_must_be_8(self):
        from taxi.forms import DriverCreationForm
        form = DriverCreationForm(
            data={
                "username": "u1",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "license_number": "AB1234",  # 6 символів
                "first_name": "A",
                "last_name": "B",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_first_three_must_be_uppercase_letters(self):
        from taxi.forms import DriverCreationForm
        # не всі великі / не всі літери
        for lic in ("abC12345", "A1C12345"):
            form = DriverCreationForm(
                data={
                    "username": f"u_{lic}",
                    "password1": "StrongPass123",
                    "password2": "StrongPass123",
                    "license_number": lic,
                    "first_name": "A",
                    "last_name": "B",
                }
            )
            self.assertFalse(form.is_valid(), f"Should be invalid for {lic}")
            self.assertIn("license_number", form.errors)

    def test_license_last_five_must_be_digits(self):
        from taxi.forms import DriverCreationForm
        form = DriverCreationForm(
            data={
                "username": "u2",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "license_number": "ABC12x45",  # не всі цифри в останніх 5
                "first_name": "A",
                "last_name": "B",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_required_fields_present(self):
        from taxi.forms import DriverCreationForm
        form = DriverCreationForm()
        fields = set(form.fields.keys())
        # Перевіряємо, що ключові поля є у формі
        for name in {
            "username",
            "password1",
            "password2",
            "license_number",
            "first_name",
            "last_name"
        }:
            self.assertIn(name, fields)


class DriverLicenseUpdateFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="upduser",
            password="x",
            license_number="ABC12345",
            first_name="Up",
            last_name="Dater",
        )

    def test_update_with_valid_license(self):
        from taxi.forms import DriverLicenseUpdateForm
        form = DriverLicenseUpdateForm(
            data={"license_number": "DEF67890"}, instance=self.user
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.license_number, "DEF67890")

    def test_update_rejects_invalid_license(self):
        from taxi.forms import DriverLicenseUpdateForm
        form = DriverLicenseUpdateForm(
            data={"license_number": "DE67880"}, instance=self.user  # коротке
        )
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
