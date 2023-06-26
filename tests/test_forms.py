from django.test import TestCase

from taxi.forms import CarSearchForm


class CarSearchFormTests(TestCase):
    def test_car_search_form(self) -> None:
        form_data = {"model": "Test model"}
        form = CarSearchForm(data=form_data)
        self.assertTrue(form.is_valid())  # Assert that the form is valid

        self.assertEqual(
            form.cleaned_data["model"], "Test model"
        )  # Assert form field values

        model_field = form.fields["model"]
        self.assertEqual(model_field.label, "")
        self.assertEqual(model_field.required, False)
        self.assertEqual(
            model_field.widget.attrs.get("placeholder"), "Search by model.."
        )
