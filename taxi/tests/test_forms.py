from django.test import TestCase

from taxi.forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm


class FormsTests(TestCase):
    def test_car_search_form_is_valid(self):
        form_data = {"model": "chifferiferrari"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "chifferiferrari")

    def test_driver_form_is_valid(self):
        form_data = {"username": "permanganates"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "permanganates")

    def test_manufacturer_form_is_valid(self):
        form_data = {"name": "Pasta"}
        form = ManufacturerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Pasta")
