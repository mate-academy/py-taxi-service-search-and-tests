from django.test import TestCase

from taxi.forms import CarSearchForm, ManufacturerSearchForm, DriverSearchForm


class TestCarSearchForm(TestCase):
    def setUp(self) -> None:
        self.form_data = form_data = {
            "model": "Camry"
        }
        self.form = CarSearchForm(data=form_data)

    def test_search_form_cars_valid(self) -> None:
        self.assertTrue(self.form.is_valid())
        self.assertEquals(
            self.form.cleaned_data["model"],
            self.form_data["model"]
        )


class TestManufacturerSearchForm(TestCase):
    def setUp(self) -> None:
        self.form_data = form_data = {
            "name": "TestName"
        }
        self.form = ManufacturerSearchForm(data=form_data)

    def test_search_form_cars_valid(self) -> None:
        self.assertTrue(self.form.is_valid())
        self.assertEquals(
            self.form.cleaned_data["name"],
            self.form_data["name"]
        )


class TestDriverSearchForm(TestCase):
    def setUp(self) -> None:
        self.form_data = form_data = {
            "username": "TestUserName"
        }
        self.form = DriverSearchForm(data=form_data)

    def test_search_form_cars_valid(self) -> None:
        self.assertTrue(self.form.is_valid())
        self.assertEquals(
            self.form.cleaned_data["username"],
            self.form_data["username"]
        )
