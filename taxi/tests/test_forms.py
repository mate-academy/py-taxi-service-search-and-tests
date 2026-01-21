from django.test import TestCase

from taxi.forms import DriverSearchForm, ManufacturerSearchForm, CarSearchForm


class SearchFormTest(TestCase):
    def test_manufacturer_search_form_valid(self):
        form_data = {"name": "testname"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "testname")

    def test_manufacturer_search_form_empty(self):
        form_data = {"name": ""}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_manufacturer_search_form_widget(self):
        form = ManufacturerSearchForm()
        self.assertEqual(
            form.fields["name"].widget.attrs["placeholder"],
            "Search by name"
        )

    def test_car_search_form_valid(self):
        form_data = {"model": "test"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "test")

    def test_car_search_form_empty(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_car_search_form_widget(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "Search by model"
        )

    def test_driver_search_form_valid(self):
        form_data = {"username": "testuser"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_driver_search_form_empty(self):
        form_data = {"username": ""}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_driver_search_form_widget(self):
        form = DriverSearchForm()
        self.assertEqual(
            form.fields["username"].widget.attrs["placeholder"],
            "Search by username"
        )
