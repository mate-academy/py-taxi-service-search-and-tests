from django.test import TestCase
from taxi.forms import DriverSearchForm, CarSearchForm


class DriverSearchFormTest(TestCase):
    def test_valid_data(self):
        form = DriverSearchForm({"name": "test_driver"})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = DriverSearchForm({})
        self.assertTrue(form.is_valid())

    def test_long_name(self):
        # Use a string that's too long for the name field
        name = "a" * 256
        form = DriverSearchForm({"name": name})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "name": [
                    "Ensure this value has at most 255 characters "
                    "(it has 256)."
                ],
            },
        )


class CarSearchFormTest(TestCase):
    def test_valid_data(self):
        form = CarSearchForm({"model": "Tesla Model S"})
        self.assertTrue(form.is_valid())

    def test_empty_data(self):
        form = CarSearchForm({})
        self.assertTrue(form.is_valid())

    def test_long_model_name(self):
        # Use a string that's too long for the model field
        model = "a" * 256
        form = CarSearchForm({"model": model})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "model": [
                    "Ensure this value has at most 255 characters "
                    "(it has 256)."
                ],
            },
        )
