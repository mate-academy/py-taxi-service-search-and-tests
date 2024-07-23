from django.test import TestCase
from taxi.forms import ManufacturerNameSearchForm


class ManufacturerNameSearchFormTest(TestCase):
    def test_form_field_max_length(self):
        form = ManufacturerNameSearchForm()
        self.assertEqual(form.fields["name"].max_length, 255)

    def test_form_field_not_required(self):
        form = ManufacturerNameSearchForm()
        self.assertFalse(form.fields["name"].required)
