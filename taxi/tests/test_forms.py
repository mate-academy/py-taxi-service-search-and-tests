from django.test import TestCase
from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm


class FormTests(TestCase):
    def test_manufacturer_search_form_field_is_not_required(self):
        form = ManufacturerSearchForm()
        self.assertFalse(form.fields["name"].required)

    def test_car_search_form_field_is_not_required(self):
        form = CarSearchForm()
        self.assertFalse(form.fields["model"].required)

    def test_driver_search_form_field_is_not_required(self):
        form = DriverSearchForm()
        self.assertFalse(form.fields["username"].required)
