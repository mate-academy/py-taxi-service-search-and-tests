from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer
from taxi.forms import (DriverCreationForm,
                        CarForm,
                        CarSearchForm,
                        DriverSearchForm,
                        ManufacturerSearchForm)


class FormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASD12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_creation_form(self):
        manufacturer = Manufacturer.objects.create(
            name="Test_manufacturer",
            country="Test_country"
        )
        user = get_user_model().objects.create_user(
            username="test_username",
            password="test123",
            license_number="ASD12345"
        )
        form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [user.id, ]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_list_search_form(self):
        form = CarSearchForm()
        self.assertTrue("model" in form.fields)
        self.assertTrue(form.fields["model"].required is False)
        self.assertTrue(form.fields["model"].widget.attrs["placeholder"])

    def test_driver_list_search_form(self):
        form = DriverSearchForm()
        self.assertTrue("username" in form.fields)
        self.assertTrue(form.fields["username"].required is False)
        self.assertTrue(form.fields["username"].widget.attrs["placeholder"])

    def test_manufacturer_list_search_form(self):
        form = ManufacturerSearchForm()
        self.assertTrue("name" in form.fields)
        self.assertTrue(form.fields["name"].required is False)
        self.assertTrue(form.fields["name"].widget.attrs["placeholder"])
