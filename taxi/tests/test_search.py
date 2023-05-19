from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm


class SearchFormsTests(TestCase):
    def test_driver_search_form_with_data_is_valid(self):
        form_data = {
            "username": "test_user"
        }
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_search_form_without_data_is_valid(self):
        form_data = {}
        form = DriverSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_driver_search_form_placeholder_attribute(self):
        form = DriverSearchForm()

        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "search by username",
        )

    def test_car_search_form_with_data_is_valid(self):
        form_data = {
            "model": "TestModel"
        }
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_search_form_without_data_is_valid(self):
        form_data = {}
        form = CarSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_car_search_form_placeholder_attribute(self):
        form = CarSearchForm()

        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "search by model",
        )

    def test_manufacturer_search_form_with_data_is_valid(self):
        form_data = {
            "name": "Manufacturer"
        }
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_without_data_is_valid(self):
        form_data = {}
        form = ManufacturerSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_placeholder_attribute(self):
        form = ManufacturerSearchForm()

        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "search by name"
        )
