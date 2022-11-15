from django.test import TestCase


from taxi.forms import DriverCreationForm, CarSearchForm, DriverSearchForm, \
    ManufacturerSearchForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_first_last_name_is_valid(self):
        form_data = {
            "username": "User12345",
            "password1": "usertest0987",
            "password2": "usertest0987",
            "license_number": "ADC10293",
            "first_name": "User",
            "last_name": "Test"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_creation_form_with_license_is_not_valid(self):
        form_data = {
            "username": "User12345",
            "password1": "usertest0987",
            "password2": "usertest0987",
            "license_number": "ADC1093",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)

    def test_car_search_form(self):
        form_data = {"model": "testing123"}
        form = CarSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_manufacturer_search_form(self):
        form_data = {"name": "manuf321"}
        form = ManufacturerSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_search_form(self):
        form_data = {"username": "user123"}
        form = DriverSearchForm(form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
