from django.test import TestCase
from taxi.forms import ManufacturerSearchForm


class ManufacturerSearchFormTests(TestCase):
    def test_form_valid_with_valid_data(self):
        form_data = {"name": "Toyota"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Toyota")

    def test_form_invalid_with_empty_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_form_invalid_with_empty_name(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_placeholder_attribute(self):
        form = ManufacturerSearchForm()
        widget = form.fields["name"].widget
        self.assertEqual(widget.attrs["placeholder"], "name")
