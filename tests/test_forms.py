from django.test import TestCase

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm


class ManufacturerSearchFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "name": "Test Manufacturer",
        }
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form_data = {}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_widget_attrs(self):
        form = ManufacturerSearchForm()
        name_widget = form.fields["name"].widget
        self.assertIn("placeholder", name_widget.attrs)
        self.assertEqual(name_widget.attrs["placeholder"], "search by name")


class CarSearchFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "model": "Test Model",
        }
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form_data = {}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_widget_attrs(self):
        form = CarSearchForm()
        model_widget = form.fields["model"].widget
        self.assertIn("placeholder", model_widget.attrs)
        self.assertEqual(model_widget.attrs["placeholder"], "search by model")


class DriverSearchFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            "username": "TestUsername",
        }
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_data(self):
        form_data = {}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_widget_attrs(self):
        form = DriverSearchForm()
        username_widget = form.fields["username"].widget
        self.assertIn("placeholder", username_widget.attrs)
        self.assertEqual(
            username_widget.attrs["placeholder"],
            "search by username",
        )
