from django.test import SimpleTestCase

from taxi.forms import (
    CarSearchForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)


class SearchFormsTests(SimpleTestCase):

    # --- ManufacturerSearchForm ---
    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Toyota"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_placeholder_using_str(self):
        form = ManufacturerSearchForm()
        placeholder = str(form.fields["name"].widget.attrs.get("placeholder"))
        self.assertEqual(placeholder, "Search by manufacturer name...")

    # --- CarSearchForm ---
    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Camry"})
        self.assertTrue(form.is_valid())

    def test_car_search_form_placeholder_using_str(self):
        form = CarSearchForm()
        placeholder = str(form.fields["model"].widget.attrs.get("placeholder"))
        self.assertEqual(placeholder, "Search by car model...")

    # --- DriverSearchForm ---
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "john_doe"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_placeholder_using_str(self):
        form = DriverSearchForm()
        placeholder = str(
            form.fields["username"].widget.attrs.get("placeholder")
        )
        self.assertEqual(placeholder, "Search by username...")
