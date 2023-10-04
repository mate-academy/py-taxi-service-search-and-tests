from django.contrib.auth import get_user_model
from django.forms import forms
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverLicenseUpdateForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm,
    DriverSearchForm,
)
from taxi.models import Car, Manufacturer


class DriverLicenseUpdateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            license_number="INK37261",
        )
        self.client.force_login(self.user)

    def test_form_must_work_with_correct_input_and_redirect(self):
        new_number = "JLM43534"
        form_data = {"license_number": new_number}
        form = DriverLicenseUpdateForm(data=form_data)
        url = reverse("taxi:driver-update", args=[self.user.id])
        res = self.client.post(url, form.data)
        self.user.refresh_from_db()
        self.assertRedirects(res, reverse("taxi:driver-list"))
        self.assertEquals(self.user.license_number, new_number)

    def test_form_must_raise_correct_exceptions(self):
        form = DriverLicenseUpdateForm(data={"license_number": "QSF4321"})
        self.assertEquals(
            form.errors.get("license_number"),
            ["License number should consist of 8 characters"],
        )
        form = DriverLicenseUpdateForm(data={"license_number": "acv43521"})
        self.assertEquals(
            form.errors.get("license_number"),
            ["First 3 characters should be uppercase letters"],
        )
        form = DriverLicenseUpdateForm(data={"license_number": "AC243521"})
        self.assertEquals(
            form.errors.get("license_number"),
            ["First 3 characters should be uppercase letters"],
        )
        form = DriverLicenseUpdateForm(data={"license_number": "ACDZ3521"})
        self.assertEquals(
            form.errors.get("license_number"),
            ["Last 5 characters should be digits"],
        )


class DriverCreationFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            license_number="INK37261",
        )
        self.client.force_login(self.user)
        manuf = Manufacturer.objects.create(name="Test_prod", country="Some")
        self.car = Car.objects.create(model="test_car", manufacturer=manuf)

    @staticmethod
    def get_form_data(license_number: str) -> dict:
        return {
            "username": "test_2",
            "license_number": license_number,
            "first_name": "test_first",
            "last_name": "test_last",
            "password1": "fwa32324a@!",
            "password2": "fwa32324a@!",
        }

    def test_form_must_work_with_correct_input(self):
        form = DriverLicenseUpdateForm(data=self.get_form_data("UVK48923"))
        url = reverse("taxi:driver-create")
        self.client.post(url, form.data)
        self.assertTrue(
            get_user_model().objects.filter(username="test_2").exists()
        )
        user = get_user_model().objects.get(username="test_2")
        self.assertEquals(user.license_number, "UVK48923")
        self.assertEquals(user.first_name, "test_first")
        self.assertEquals(user.last_name, "test_last")
        self.assertTrue(user.check_password("fwa32324a@!"))

    def test_form_must_raise_correct_exceptions(self):
        form = DriverLicenseUpdateForm(data=self.get_form_data("JLM4353434"))
        self.assertEquals(
            form.errors.get("license_number"),
            ["License number should consist of 8 characters"],
        )

        form = DriverLicenseUpdateForm(data=self.get_form_data("vne43534"))
        self.assertEquals(
            form.errors.get("license_number"),
            ["First 3 characters should be uppercase letters"],
        )

        form = DriverLicenseUpdateForm(data=self.get_form_data("AC243521"))
        self.assertEquals(
            form.errors.get("license_number"),
            ["First 3 characters should be uppercase letters"],
        )

        form = DriverLicenseUpdateForm(data=self.get_form_data("DIENF321"))
        self.assertEquals(
            form.errors.get("license_number"),
            ["Last 5 characters should be digits"],
        )


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="freaoiewj",
            password="feoiaw408#f",
            license_number="INK37261",
        )
        self.client.force_login(self.user)
        manuf = Manufacturer.objects.create(name="Test_prod", country="Some")
        self.car = Car.objects.create(model="test_car", manufacturer=manuf)

    def test_drivers_field_config(self):
        form = CarForm()
        self.assertIn(
            "forms.widgets.CheckboxSelectMultiple object",
            str(form.fields.get("drivers").widget),
        )
        self.assertEquals(
            len(form.fields.get("drivers").queryset),
            get_user_model().objects.all().count(),
        )

    def test_create_form_works(self):
        form = CarForm(
            data={
                "model": "new_test_car",
                "manufacturer": 1,
                "drivers": [
                    1,
                ],
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(reverse("taxi:car-create"), form.data)
        self.assertTrue(Car.objects.filter(model="new_test_car").exists())

    def test_update_form_works(self):
        form = CarForm(
            data={
                "model": "old_updated_test_car",
                "manufacturer": 1,
                "drivers": [
                    1,
                ],
            }
        )
        self.assertTrue(form.is_valid())
        self.client.post(reverse("taxi:car-update", args=[1]), form.data)
        self.assertTrue(
            Car.objects.filter(model="old_updated_test_car").exists()
        )


class SearchFormsTest(TestCase):
    """Logic behind those bellow is tested in the views section"""

    def test_car_searchform_config(self):
        form = CarSearchForm(data={"model": "0"})
        self.assertEquals(form.fields.get("model").label, "")
        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("model").widget),
        )
        self.assertIn("placeholder", form.fields.get("model").widget.attrs)

    def test_driver_searchform_config(self):
        form = DriverSearchForm(data={"username": "0"})
        self.assertEquals(form.fields.get("username").label, "")
        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("username").widget),
        )
        self.assertIn("placeholder", form.fields.get("username").widget.attrs)

    def test_manufacturer_searchform_config(self):
        form = ManufacturerSearchForm(data={"name": "0"})
        self.assertEquals(form.fields.get("name").label, "")
        self.assertIn(
            "forms.widgets.TextInput object",
            str(form.fields.get("name").widget),
        )
        self.assertIn("placeholder", form.fields.get("name").widget.attrs)
