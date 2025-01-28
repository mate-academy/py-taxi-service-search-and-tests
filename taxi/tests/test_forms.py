from django.test import TestCase

from django.contrib.auth import get_user_model

from taxi.models import Manufacturer
from taxi.forms import CarForm, CarModelSearchForm


class CarFormTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="testpas123", license_number="ABCDEF132"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="testpas123", license_number="ABCDEF123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer1",
            country="country"
        )
        self.car_data = {
            "model": "Tesla Model S",
            "manufacturer": self.manufacturer
        }

    def test_valid_form(self):
        form_data = self.car_data.copy()
        form_data["drivers"] = [self.user1.id, self.user2.id]
        form = CarForm(data=form_data)

        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_missing_required_fields(self):
        form = CarForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)
        self.assertIn("manufacturer", form.errors)

    def test_save_form(self):
        form_data = self.car_data.copy()
        form_data["drivers"] = [self.user1.id, self.user2.id]
        form = CarForm(data=form_data)

        car = form.save()
        self.assertEqual(car.model, "Tesla Model S")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertEqual(list(car.drivers.all()), [self.user1, self.user2])


class CarModelSearchTests(TestCase):
    def setUp(self):
        self.car_search_data = {
            "model": "Tesla Model S",
        }

    def test_valid_form(self):
        form_data = self.car_search_data.copy()
        form_data["model"] = "Tesla Model S"
        form = CarModelSearchForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
