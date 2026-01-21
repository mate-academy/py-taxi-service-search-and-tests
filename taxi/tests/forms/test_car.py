from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="user1",
            password="1234",
            license_number="NBA12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="user2",
            password="1234",
            license_number="NBA12346"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="Manufacturer",
            country="Country"
        )

    def test_form_initialization(self):
        driver_field = CarForm().fields["drivers"]
        self.assertEqual(
            driver_field.queryset.count(),
            get_user_model().objects.count()
        )
        self.assertIsInstance(
            driver_field.widget,
            forms.CheckboxSelectMultiple
        )

    def test_form_valid_data(self):
        form_data = {
            "model": "Test",
            "manufacturer": self.manufacturer,
            "drivers": [self.driver1, self.driver2],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            "model": "Test",
            "manufacturer": self.manufacturer,
            "drivers": [9999],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)
