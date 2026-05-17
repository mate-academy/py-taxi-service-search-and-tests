from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class SearchFormsTest(TestCase):
    def test_driver_search_form_field_label(self):
        form = DriverSearchForm()
        self.assertEqual(form.fields["username"].label, "")

    def test_car_search_form_field_label(self):
        form = CarSearchForm()
        self.assertEqual(form.fields["model"].label, "")

    def test_manufacturer_search_form_field_label(self):
        form = ManufacturerSearchForm()
        self.assertEqual(form.fields["name"].label, "")

    def test_driver_search_form_placeholder(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )
