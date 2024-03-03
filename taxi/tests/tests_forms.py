from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import (DriverCreationForm,
                        DriverLicenseUpdateForm,
                        CarSearchForm,
                        DriverSearchForm,
                        ManufacturerSearchForm,
                        CarForm)
from taxi.models import Manufacturer


class FormsTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "test first_name",
            "last_name": "test last_name",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_license_update_form_is_valid(self):
        form_data = {
            "license_number": "ZXC78945"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarSearchFormTest(TestCase):
    def test_car_search_form_rendering(self):
        form = CarSearchForm()
        expected_html = (
            "<input type='text' name='model' "
            "placeholder='Search by model' maxlength='255' "
            "id='id_model'>"
        )
        self.assertHTMLEqual(str(form["model"]), expected_html)

    def test_car_search_form_validation(self):
        form_data = {
            "model": "Lincoln"
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverSearchFormTest(TestCase):
    def test_driver_search_form_rendering(self):
        form = DriverSearchForm()
        expected_html = (
            "<input type='text' name='username' "
            "placeholder='Search by username' maxlength='255' "
            "id='id_username'>"
        )
        self.assertHTMLEqual(str(form["username"]), expected_html)

    def test_driver_search_form_validation(self):
        form_data = {
            "username": "admin"
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class ManufacturerSearchFormTest(TestCase):
    def test_manufacturer_search_form_rendering(self):
        form = ManufacturerSearchForm()
        expected_html = (
            "<input type='text' name='name' "
            "placeholder='Search by name' maxlength='255' "
            "id='id_name'>"
        )
        self.assertHTMLEqual(str(form["name"]), expected_html)

    def test_manufacturer_search_form_validation(self):
        form_data = {
            "name": "Subaru"
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="test",
                                                        country="test")
        self.driver1 = get_user_model().objects.create(
            username="test1",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create(
            username="test2",
            license_number="CBA54321"
        )

    def test_car_creation_form_valid(self):
        drivers = get_user_model().objects.filter(id__in=[self.driver1.id,
                                                          self.driver2.id])
        form_data = {
            "model": "test",
            "manufacturer": self.manufacturer,
            "drivers": drivers,
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(str(form.cleaned_data), str(form_data))
