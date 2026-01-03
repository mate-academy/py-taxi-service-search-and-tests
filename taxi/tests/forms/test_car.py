from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm
from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self):
        self.bob = get_user_model().objects.create_user(
            username="bob",
            password="123",
            license_number="CCC12345"
        )
        self.bob2 = get_user_model().objects.create_user(
            username="bob2",
            password="123",
            license_number="CCC12346"
        )

        self.mercedes = Manufacturer.objects.create(
            name="Mercedes",
            country="Germany"
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
            "model": "Golf",
            "manufacturer": self.mercedes,
            "drivers": list(get_user_model().objects.all())
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            "model": "invalid",
            "manufacturer": self.mercedes,
            "drivers": [17171]
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("drivers", form.errors)
