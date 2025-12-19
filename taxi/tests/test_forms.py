from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.forms import CarSearchForm, CarForm
from taxi.models import Manufacturer


class CarSearchFormTest(TestCase):
    def test_search_form_valid(self):
        form = CarSearchForm(data={"model": "BMW"})
        self.assertTrue(form.is_valid())

    def test_search_form_empty(self):
        form = CarSearchForm(data={"model": ""})
        self.assertTrue(form.is_valid())


class CarFormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_car_form_valid(self):
        user = get_user_model().objects.create(username="testuser")
        manufacturer = Manufacturer.objects.create(name="BMW")

        form_data = {
            "model": "X5",
            "manufacturer": manufacturer.id,
            "drivers": [user.id],
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid(self):
        form = CarForm(data={
            "model": "",
            "manufacturer": ""
        })
        self.assertFalse(form.is_valid())
