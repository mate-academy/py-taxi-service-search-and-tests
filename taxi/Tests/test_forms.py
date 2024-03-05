from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        CarSearchForm,
                        ManufacturerSearchForm,
                        DriverSearchForm,
                        CarForm
                        )
from taxi.models import Manufacturer, Driver


class FormTests(TestCase):
    def test_form_validity(self):
        form_data = {
            "username": "new_user",
            "password1": "testing123new",
            "password2": "testing123new",
            "license_number": "NEW12345",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, form_data)

    def test_update_license_number(self):
        new_license_form = {
            "license_number": "NEW12345",
        }
        form = DriverLicenseUpdateForm(data=new_license_form)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data, new_license_form)


class CarSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = CarSearchForm()
        expected_html = (
            "<input type='text' name='car_model' "
            "placeholder='Search by model' maxlength='255' "
            "id='id_car_model'>"
        )
        self.assertHTMLEqual(str(form["car_model"]), expected_html)

    def test_form_validation(self):
        form = CarSearchForm(data={"car_model": "Corolla"})
        self.assertTrue(form.is_valid())
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())


class ManufacturerSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = ManufacturerSearchForm()
        expected_html = (
            "<input type='text' name='manufacturer_name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_manufacturer_name'>"
        )
        self.assertHTMLEqual(str(form["manufacturer_name"]), expected_html)

    def test_form_validation(self):
        form = CarSearchForm(data={"manufacturer_name": "BMW"})
        self.assertTrue(form.is_valid())
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())


class DriverSearchFormTest(TestCase):
    def test_form_rendering(self):
        form = DriverSearchForm()
        expected_html = (
            "<input type='text' name='username' "
            "placeholder='Search by username' maxlength='255' "
            "id='id_username'>"
        )
        self.assertHTMLEqual(str(form["username"]), expected_html)

    def test_form_validation(self):
        form = CarSearchForm(data={"username": "admin1"})
        self.assertTrue(form.is_valid())
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.driver1 = Driver.objects.create(
            username="John",
            license_number="NKG65214"
        )
        self.driver2 = Driver.objects.create(
            username="Alice",
            license_number="NKL65204"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
