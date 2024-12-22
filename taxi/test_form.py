from django import forms
from django.test import TestCase
from .forms import CarSearchForm


class CarSearchFormTestCase(TestCase):
    def test_form_valid_with_data(self):
        form_data = {"model": "Toyota"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")

    def test_form_valid_with_empty_data(self):
        form_data = {"model": ""}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_form_has_placeholder(self):
        form = CarSearchForm()
        self.assertIn("placeholder", form["model"].field.widget.attrs)
        self.assertEqual(
            form["model"].field.widget.attrs["placeholder"],
            "Search car"
        )
