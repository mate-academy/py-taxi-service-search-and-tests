from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class TestDriverSearchForm(TestCase):
    def test_valid_username_search(self):
        form_data = {'username': 'test_user'}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'test_user')


class TestCarSearchForm(TestCase):
    def test_valid_model_search(self):
        form_data = {'model': 'test_model'}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['model'], 'test_model')


class TestManufacturerSearchForm(TestCase):
    def test_valid_name_search(self):
        form_data = {'name': 'test_manufacturer'}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'test_manufacturer')
