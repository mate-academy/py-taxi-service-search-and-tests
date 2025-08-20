from django.test import TestCase

from taxi.forms import DriverUsernameForm, CarModelForm, ManufacturerNameForm


class FormTest(TestCase):
    def test_driver_search_form(self):
        username = {"username": "admin.user"}
        username_search = DriverUsernameForm(data=username)
        self.assertTrue(username_search.is_valid())
        self.assertEqual(username_search.cleaned_data, username)

    def test_car_search_form(self):
        model = {"model": "Lincoln"}
        model_search = CarModelForm(data=model)
        self.assertTrue(model_search.is_valid())
        self.assertEqual(model_search.cleaned_data, model)

    def test_manufacturer_search_form(self):
        name = {"name": "BMW"}
        name_search = ManufacturerNameForm(data=name)
        self.assertTrue(name_search.is_valid())
        self.assertEqual(name_search.cleaned_data, name)
